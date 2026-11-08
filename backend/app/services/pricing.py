from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from backend.app.models import Product
from backend.app.config import settings

def compute_unit_price(product: Product, chosen_term: int) -> int:
    """
    Term-based pricing rule:
    - 24 months: price_min
    - 12 months: midpoint of min and max (or price_min if min contract is 24)
    - Minimum contract (flexible < 12m): price_max
    """
    if chosen_term >= 24:
        return product.price_min
    elif chosen_term == 12:
        if product.min_contract_months >= 24:
            return product.price_min
        return round((product.price_min + product.price_max) / 2)
    else:
        return product.price_max

def calculate_promised_date(active_products: List[Product], base_date_str: Optional[str] = None) -> str:
    base_str = base_date_str or settings.DEMO_TODAY
    base_dt = datetime.strptime(base_str, "%Y-%m-%d")
    max_install_days = max([p.install_days for p in active_products], default=3)
    promised_dt = base_dt + timedelta(days=1 + max_install_days)
    return promised_dt.strftime("%Y-%m-%d")

def calculate_quote(
    active_items: List[Dict[str, Any]],  # list of {'product': Product, 'qty': int, 'why': str, ...}
    term_months: int = 12,
    current_spend: Optional[float] = None
) -> Dict[str, Any]:
    """
    Computes all pricing totals rounded to whole rupees.
    """
    monthly_recurring = 0
    one_time_setup = 0
    bundle_lines = []

    for item in active_items:
        product: Product = item["product"]
        qty = item.get("qty", 1)
        unit_price = compute_unit_price(product, term_months)
        line_total = unit_price * qty
        line_setup = product.setup_fee * qty

        monthly_recurring += line_total
        one_time_setup += line_setup

        bundle_lines.append({
            "product_id": product.product_id,
            "category": product.category,
            "name_plain": product.product_name,
            "qty": qty,
            "unit": product.unit,
            "unit_price": unit_price,
            "line_total": line_total,
            "setup_fee": line_setup,
            "why": item.get("why", ""),
            "min_contract_months": product.min_contract_months,
            "can_toggle": item.get("can_toggle", True),
            "active": True
        })

    gst_amount = round(0.18 * monthly_recurring)
    gst_setup = round(0.18 * one_time_setup)
    first_invoice = monthly_recurring + one_time_setup + gst_amount + gst_setup
    tco_term = (monthly_recurring * term_months) + one_time_setup + round(0.18 * ((monthly_recurring * term_months) + one_time_setup))

    vs_current_spend = None
    if current_spend is not None and current_spend > 0:
        vs_current_spend = round(current_spend - monthly_recurring, 2)

    active_prods = [item["product"] for item in active_items]
    promised_date = calculate_promised_date(active_prods)

    return {
        "term_months": term_months,
        "monthly_recurring": monthly_recurring,
        "one_time_setup": one_time_setup,
        "gst_amount": gst_amount,
        "first_invoice": first_invoice,
        "tco_term": tco_term,
        "vs_current_spend": vs_current_spend,
        "promised_date": promised_date,
        "bundle": bundle_lines
    }
