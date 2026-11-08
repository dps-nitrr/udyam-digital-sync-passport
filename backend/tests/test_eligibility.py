import pytest
import json
from sqlmodel import Session, select
from backend.app.db import engine
from backend.app.models import Product
from backend.app.services.eligibility import check_product_eligibility, validate_bundle

@pytest.fixture
def session():
    with Session(engine) as s:
        yield s

def test_rule_city_tier(session):
    # Find a product with limited tiers
    products = session.exec(select(Product)).all()
    # P05 leased line or similar
    prod = next((p for p in products if "tier_2" not in p.tiers), products[0])
    
    ctx_fail = {"city_tier": "tier_3", "employees": 50, "sites": 10, "has_active_gstin": True, "bundle_product_ids": []}
    ok, reasons, _ = check_product_eligibility(prod, ctx_fail)
    assert not ok
    assert "tier_not_served" in reasons

def test_rule_min_employees(session):
    # Find product with min_employees > 1
    products = session.exec(select(Product)).all()
    prod = next(p for p in products if p.min_employees > 1)
    
    ctx_fail = {"city_tier": prod.tiers[0], "employees": prod.min_employees - 1, "sites": 10, "has_active_gstin": True, "bundle_product_ids": []}
    ok, reasons, _ = check_product_eligibility(prod, ctx_fail)
    assert not ok
    assert "too_small" in reasons
    
    ctx_pass = {"city_tier": prod.tiers[0], "employees": prod.min_employees, "sites": 10, "has_active_gstin": True, "bundle_product_ids": prod.requires_one_of}
    ok, reasons, _ = check_product_eligibility(prod, ctx_pass)
    assert "too_small" not in reasons

def test_rule_min_sites(session):
    products = session.exec(select(Product)).all()
    prod = next(p for p in products if p.min_sites > 1)
    
    ctx_fail = {"city_tier": prod.tiers[0], "employees": 50, "sites": prod.min_sites - 1, "has_active_gstin": True, "bundle_product_ids": prod.requires_one_of}
    ok, reasons, _ = check_product_eligibility(prod, ctx_fail)
    assert not ok
    assert "too_few_sites" in reasons

def test_rule_requires_gstin(session):
    products = session.exec(select(Product)).all()
    prod = next(p for p in products if p.requires_gstin)
    
    ctx_fail = {"city_tier": prod.tiers[0], "employees": 50, "sites": 10, "has_active_gstin": False, "bundle_product_ids": prod.requires_one_of}
    ok, reasons, _ = check_product_eligibility(prod, ctx_fail)
    assert not ok
    assert "needs_gstin" in reasons

def test_rule_requires_one_of_all_catalogue_rows(session):
    products = session.exec(select(Product)).all()
    dep_products = [p for p in products if len(p.requires_one_of) > 0]
    assert len(dep_products) > 0, "Expected at least one product with dependencies"

    for prod in dep_products:
        # 1. Fail when empty bundle
        ctx_fail = {
            "city_tier": prod.tiers[0],
            "employees": max(prod.min_employees, 10),
            "sites": max(prod.min_sites, 5),
            "has_active_gstin": True,
            "bundle_product_ids": []
        }
        ok, reasons, _ = check_product_eligibility(prod, ctx_fail)
        assert not ok, f"Product {prod.product_id} should fail without dependencies"
        assert "needs_dependency" in reasons

        # 2. Pass dependency check when one valid dependency is added
        for dep_id in prod.requires_one_of:
            ctx_pass = dict(ctx_fail)
            ctx_pass["bundle_product_ids"] = [dep_id]
            ok, reasons, _ = check_product_eligibility(prod, ctx_pass)
            assert "needs_dependency" not in reasons, f"Product {prod.product_id} should satisfy dependency with {dep_id}"
