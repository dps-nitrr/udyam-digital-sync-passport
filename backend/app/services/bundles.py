from typing import Dict, Any, List, Tuple
from sqlmodel import Session, select
from backend.app.models import Product
from backend.app.services.eligibility import check_product_eligibility

BUNDLE_TEMPLATES = {
    "Small multi-site businesses": {
        "default_term": 24,
        "core": [
            {"product_id": "P02", "qty_formula": lambda e, s: s, "rule_id": "MS-FIBRE", "why": "High-speed business fibre for branch operations"},
            {"product_id": "P09", "qty_formula": lambda e, s: s, "rule_id": "MS-FAILOVER", "why": "Your shop closes if the internet drops — 4G failover keeps billing alive"},
            {"product_id": "P08", "qty_formula": lambda e, s: max(1, min(e, 5)), "rule_id": "MS-LINES", "why": "Dedicated multi-channel calling lines for branch desks"},
            {"product_id": "P22", "qty_formula": lambda e, s: s, "rule_id": "MS-WIFI", "why": "Cloud-managed secure Wi-Fi for staff and customers across all stores"},
            {"product_id": "P10", "condition": lambda e, s: s >= 3 and e >= 10, "qty_formula": lambda e, s: 1, "rule_id": "MS-SDWAN", "why": "Centralized SD-WAN control across all 3+ branches"}
        ],
        "addons": [
            {"product_id": "P23", "qty_formula": lambda e, s: 2 * s, "rule_id": "MS-CCTV", "why": "Cloud-connected CCTV cameras for branch security"},
            {"product_id": "P20", "qty_formula": lambda e, s: e, "rule_id": "MS-ENDPOINT", "why": "Antivirus and ransomware endpoint protection for store PCs"},
            {"product_id": "P16", "qty_formula": lambda e, s: e, "rule_id": "MS-WORKSPACE", "why": "Professional business email and cloud storage"}
        ]
    },
    "Professional offices": {
        "default_term": 12,
        "core": [
            {"product_id": "P02", "condition": lambda e, s: e >= 5, "qty_formula": lambda e, s: s, "rule_id": "PROF-FIBRE-PRO", "why": "Ultra-fast symmetric fibre for heavy client files and video calls"},
            {"product_id": "P01", "condition": lambda e, s: e < 5, "qty_formula": lambda e, s: s, "rule_id": "PROF-FIBRE-STD", "why": "High-speed reliable fibre for daily office workflow"},
            {"product_id": "P16", "qty_formula": lambda e, s: max(1, e), "rule_id": "PROF-WORKSPACE", "why": "Professional email on your custom business domain"},
            {"product_id": "P17", "qty_formula": lambda e, s: 1, "rule_id": "PROF-BACKUP", "why": "Automated cloud backup protects confidential client records"},
            {"product_id": "P20", "qty_formula": lambda e, s: max(1, e), "rule_id": "PROF-SECURITY", "why": "Complete malware & endpoint security for office computers"}
        ],
        "addons": [
            {"product_id": "P11", "qty_formula": lambda e, s: 1, "rule_id": "PROF-STATIC-IP", "why": "Static IP for VPN and remote secure server access"},
            {"product_id": "P07", "qty_formula": lambda e, s: 1, "rule_id": "PROF-VOICE", "why": "High-clarity landline for client reception"},
            {"product_id": "P12", "qty_formula": lambda e, s: 1, "rule_id": "PROF-PBX", "why": "Virtual receptionist IVR to greet clients professionally"},
            {"product_id": "P09", "qty_formula": lambda e, s: 1, "rule_id": "PROF-FAILOVER", "why": "Automatic cellular failover keeps video meetings uninterrupted"}
        ]
    },
    "Small manufacturers": {
        "default_term": 24,
        "core": [
            {"product_id": "P05", "qty_formula": lambda e, s: 1, "rule_id": "MFG-LEASED", "why": "Dedicated 1:1 leased line with 99.5% uptime SLA for factory floor"},
            {"product_id": "P21", "qty_formula": lambda e, s: 1, "rule_id": "MFG-FIREWALL", "why": "Hardware firewall shielding operational systems from intrusions"},
            {"product_id": "P09", "qty_formula": lambda e, s: 1, "rule_id": "MFG-FAILOVER", "why": "Redundant wireless connection ensures telemetry stays live"}
        ],
        "addons": [
            {"product_id": "P24", "qty_formula": lambda e, s: 1, "rule_id": "MFG-IOT", "why": "Industrial IoT sensors tracking machine uptime and power"},
            {"product_id": "P16", "qty_formula": lambda e, s: max(2, min(e, 10)), "rule_id": "MFG-WORKSPACE", "why": "Business email and document management for administrative staff"},
            {"product_id": "P20", "qty_formula": lambda e, s: max(2, min(e, 10)), "rule_id": "MFG-ENDPOINT", "why": "Antivirus defense for plant and dispatch PCs"}
        ]
    },
    "Micro retail & services": {
        "default_term": 12,
        "core": [
            {"product_id": "P04", "qty_formula": lambda e, s: 1, "rule_id": "RET-AIRFIBER", "why": "Quick wireless AirFiber setup with no cable laying wait"},
            {"product_id": "P07", "qty_formula": lambda e, s: 1, "rule_id": "RET-VOICE", "why": "Fixed telephone line for vendor and customer inquiries"},
            {"product_id": "P19", "qty_formula": lambda e, s: 1, "rule_id": "RET-POS", "why": "All-in-one POS counter machine for seamless card and UPI billing"}
        ],
        "addons": [
            {"product_id": "P18", "qty_formula": lambda e, s: 1, "rule_id": "RET-WEBSITE", "why": "Ready-to-use e-commerce store with catalog sharing"},
            {"product_id": "P22", "qty_formula": lambda e, s: 1, "rule_id": "RET-WIFI", "why": "Separate high-speed Wi-Fi hotspot for visiting customers"},
            {"product_id": "P23", "qty_formula": lambda e, s: 1, "rule_id": "RET-CCTV", "why": "Full-HD indoor security camera with mobile live view"}
        ]
    }
}

def generate_recommended_bundle(
    segment: str,
    employees: int,
    sites: int,
    city_tier: str,
    has_active_gstin: bool,
    session: Session
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], int]:
    """
    Returns:
    (active_items, excluded_items, default_term)
    """
    template_key = segment if segment in BUNDLE_TEMPLATES else "Micro retail & services"
    template = BUNDLE_TEMPLATES[template_key]
    default_term = template["default_term"]
    
    # Check if active GSTIN allows WhatsApp API in Micro retail
    core_defs = list(template["core"])
    addon_defs = list(template["addons"])

    if template_key == "Micro retail & services" and has_active_gstin:
        core_defs.append({
            "product_id": "P15",
            "qty_formula": lambda e, s: 1,
            "rule_id": "RET-WHATSAPP",
            "why": "Official WhatsApp Business API for instant bill receipts and alerts"
        })
        addon_defs.append({
            "product_id": "P14",
            "qty_formula": lambda e, s: 1,
            "rule_id": "RET-SMS",
            "why": "Bulk SMS package for promotional discount broadcasts"
        })

    # Load all products
    all_products = {p.product_id: p for p in session.exec(select(Product)).all()}
    
    candidate_core = []
    for item in core_defs:
        cond = item.get("condition")
        if cond and not cond(employees, sites):
            continue
        prod = all_products.get(item["product_id"])
        if prod:
            qty = item["qty_formula"](employees, sites)
            candidate_core.append({
                "product": prod,
                "qty": qty,
                "why": item["why"],
                "rule_id": item["rule_id"],
                "can_toggle": True,
                "active": True
            })

    candidate_addons = []
    for item in addon_defs:
        cond = item.get("condition")
        if cond and not cond(employees, sites):
            continue
        prod = all_products.get(item["product_id"])
        if prod:
            qty = item["qty_formula"](employees, sites)
            candidate_addons.append({
                "product": prod,
                "qty": qty,
                "why": item["why"],
                "rule_id": item["rule_id"],
                "can_toggle": True,
                "active": False  # default off
            })

    # Validate candidate core against eligibility engine
    ctx = {
        "city_tier": city_tier,
        "employees": employees,
        "sites": sites,
        "has_active_gstin": has_active_gstin,
        "bundle_product_ids": {c["product"].product_id for c in candidate_core}
    }

    active_items = []
    excluded_items = []

    for c in candidate_core:
        ok, reasons, plains = check_product_eligibility(c["product"], ctx)
        if ok:
            active_items.append(c)
        else:
            excluded_items.append({
                "product_id": c["product"].product_id,
                "product_name": c["product"].product_name,
                "reason_key": reasons[0] if reasons else "not_eligible",
                "reason_plain": plains[0] if plains else "Not eligible for your profile"
            })

    # Check remaining catalogue products that were excluded for visibility
    all_candidate_ids = {c["product"].product_id for c in candidate_core + candidate_addons}
    for pid, p in all_products.items():
        if pid not in all_candidate_ids:
            ok, reasons, plains = check_product_eligibility(p, ctx)
            if not ok:
                excluded_items.append({
                    "product_id": p.product_id,
                    "product_name": p.product_name,
                    "reason_key": reasons[0] if reasons else "not_applicable",
                    "reason_plain": plains[0] if plains else "Not applicable to your current segment"
                })

    return active_items, excluded_items, default_term
