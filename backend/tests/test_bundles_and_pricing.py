import pytest
import random
from sqlmodel import Session, select
from backend.app.db import engine
from backend.app.models import Lead, Product
from backend.app.services.bundles import generate_recommended_bundle
from backend.app.services.eligibility import validate_bundle
from backend.app.services.pricing import compute_unit_price, calculate_quote

def test_bundles_zero_violations_for_200_random_leads():
    with Session(engine) as session:
        leads = session.exec(select(Lead)).all()
        random.seed(123)
        sample = random.sample(leads, 200)

        for lead in sample:
            segment = lead.segment or "Micro retail & services"
            employees = lead.employee_count or 1
            sites = lead.num_sites or 1
            city_tier = lead.city_tier or "tier_1"
            has_active_gstin = True if (lead.has_gstin == "Y" and lead.gstin) else False

            active_items, excluded_items, default_term = generate_recommended_bundle(
                segment=segment,
                employees=employees,
                sites=sites,
                city_tier=city_tier,
                has_active_gstin=has_active_gstin,
                session=session
            )

            # Check that at least one product is recommended
            assert len(active_items) > 0, f"Lead {lead.lead_id} got empty bundle"

            # Validate bundle with eligibility engine
            active_products = [item["product"] for item in active_items]
            ctx = {
                "city_tier": city_tier,
                "employees": employees,
                "sites": sites,
                "has_active_gstin": has_active_gstin
            }
            violations = validate_bundle(active_products, ctx)
            assert len(violations) == 0, f"Lead {lead.lead_id} bundle has violations: {violations}"


def test_pricing_within_range_and_math_reconciliation():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        
        # 1. Price is always within [price_min, price_max]
        for p in products:
            for term in [1, 12, 24, 36]:
                u_price = compute_unit_price(p, term)
                assert p.price_min <= u_price <= p.price_max, f"Price {u_price} for {p.product_id} out of bounds [{p.price_min}, {p.price_max}]"

        # 2. Quote totals reconcile
        sample_items = [
            {"product": products[0], "qty": 2, "why": "Primary"},
            {"product": products[1], "qty": 1, "why": "Secondary"},
        ]
        quote = calculate_quote(sample_items, term_months=12, current_spend=10000)
        
        sum_lines = sum(line["line_total"] for line in quote["bundle"])
        assert sum_lines == quote["monthly_recurring"], "Sum of lines does not equal monthly_recurring"
        
        sum_setups = sum(line["setup_fee"] for line in quote["bundle"])
        assert sum_setups == quote["one_time_setup"], "Sum of setup fees does not equal one_time_setup"
        
        expected_gst = round(0.18 * quote["monthly_recurring"])
        assert quote["gst_amount"] == expected_gst, "GST math on recurring is incorrect"
        
        expected_gst_setup = round(0.18 * quote["one_time_setup"])
        expected_first_invoice = quote["monthly_recurring"] + quote["one_time_setup"] + expected_gst + expected_gst_setup
        assert quote["first_invoice"] == expected_first_invoice, "First invoice total math does not match"
