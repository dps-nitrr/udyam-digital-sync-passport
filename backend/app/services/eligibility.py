from typing import Dict, Any, List, Tuple
from backend.app.models import Product

REASON_MESSAGES = {
    "tier_not_served": "Not available in this city tier",
    "too_small": "Requires more employees than currently registered",
    "too_few_sites": "Requires multiple business locations",
    "needs_gstin": "Requires an Active GST registration",
    "needs_dependency": "Requires a prerequisite internet connection"
}

def check_product_eligibility(product: Product, ctx: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    """
    ctx = {
        'city_tier': 'tier_1' or 'tier_2',
        'employees': int,
        'sites': int,
        'has_active_gstin': bool,
        'bundle_product_ids': set or list of str
    }
    Returns: (ok: bool, reason_keys: List[str], reason_plains: List[str])
    """
    reasons = []
    reasons_plain = []
    
    city_tier = ctx.get("city_tier", "tier_1")
    employees = ctx.get("employees", 1)
    sites = ctx.get("sites", 1)
    has_active_gstin = ctx.get("has_active_gstin", False)
    bundle_product_ids = set(ctx.get("bundle_product_ids", []))

    # Rule 1: City tier
    city_tier_norm = str(city_tier).lower().replace("tier_", "").replace("tier ", "").replace("tier", "").strip()
    if product.tiers:
        prod_tiers_norm = [str(t).lower().replace("tier_", "").replace("tier ", "").replace("tier", "").strip() for t in product.tiers]
        if city_tier_norm not in prod_tiers_norm:
            reasons.append("tier_not_served")
            reasons_plain.append(f"Not available in {city_tier}")

    # Rule 2: Minimum employees
    if employees < product.min_employees:
        reasons.append("too_small")
        reasons_plain.append(f"Requires at least {product.min_employees} employees")

    # Rule 3: Minimum sites
    if sites < product.min_sites:
        reasons.append("too_few_sites")
        reasons_plain.append(f"Requires at least {product.min_sites} business locations")

    # Rule 4: Requires GSTIN
    if product.requires_gstin and not has_active_gstin:
        reasons.append("needs_gstin")
        reasons_plain.append("Requires an Active GST registration")

    # Rule 5: Requires one of (dependencies)
    req_one_of = set(product.requires_one_of)
    if req_one_of:
        # Check intersection with bundle
        if not (req_one_of & bundle_product_ids):
            reasons.append("needs_dependency")
            dep_names = " | ".join(sorted(list(req_one_of)))
            reasons_plain.append(f"Requires one of: {dep_names}")

    ok = len(reasons) == 0
    return ok, reasons, reasons_plain


def validate_bundle(bundle_products: List[Product], ctx: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validates all products in a proposed bundle against the context.
    Returns: dict mapping product_id -> list of fail reason keys.
    """
    ctx_copy = dict(ctx)
    ctx_copy["bundle_product_ids"] = {p.product_id for p in bundle_products}
    
    violations = {}
    for p in bundle_products:
        ok, reasons, _ = check_product_eligibility(p, ctx_copy)
        if not ok:
            violations[p.product_id] = reasons
            
    return violations
