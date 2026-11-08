import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.models import Journey, Quote, Product, AppEvent
from backend.app.schemas import (
    QuoteUpdateRequest,
    QuoteUpdateResponse,
    QuoteAcceptRequest,
    QuoteAcceptResponse,
    QuoteResponse,
    BundleLineItem,
    ExcludedProduct
)
from backend.app.services.pricing import calculate_quote
from backend.app.services.eligibility import check_product_eligibility, validate_bundle

router = APIRouter(prefix="/api/quote", tags=["Quote"])

@router.post("/update", response_model=QuoteUpdateResponse)
def update_quote(req: QuoteUpdateRequest, session: Session = Depends(get_session)):
    journey = session.get(Journey, req.journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    quote_obj = session.exec(select(Quote).where(Quote.journey_id == journey.id)).first()
    if not quote_obj:
        raise HTTPException(status_code=404, detail="Quote not found")

    all_products = {p.product_id: p for p in session.exec(select(Product)).all()}
    term_months = req.term_months or quote_obj.term_months

    # Read current bundle lines
    current_lines = json.loads(quote_obj.bundle_json)
    line_map = {item["product_id"]: item for item in current_lines}

    # Apply quantity updates
    if req.quantities:
        for pid, qty in req.quantities.items():
            if pid in line_map:
                line_map[pid]["qty"] = max(1, qty)

    # Apply toggle updates
    auto_added = []
    auto_removed = []
    
    if req.toggles:
        for pid, active in req.toggles.items():
            if pid in line_map:
                line_map[pid]["active"] = active
            elif active and pid in all_products:
                prod = all_products[pid]
                line_map[pid] = {
                    "product_id": pid,
                    "category": prod.category,
                    "name_plain": prod.product_name,
                    "qty": 1,
                    "unit": prod.unit,
                    "unit_price": prod.price_min,
                    "line_total": prod.price_min,
                    "setup_fee": prod.setup_fee,
                    "why": "Added by business owner",
                    "min_contract_months": prod.min_contract_months,
                    "can_toggle": True,
                    "active": True
                }

    # Dependency checking & auto-add / auto-remove
    active_ids = {pid for pid, item in line_map.items() if item.get("active", True)}
    
    # 1. Check if newly active products require dependencies
    for pid in list(active_ids):
        prod = all_products.get(pid)
        if prod and prod.requires_one_of:
            dep_set = set(prod.requires_one_of)
            if not (dep_set & active_ids):
                # Pick cheapest dependency
                dep_prods = [all_products[d] for d in prod.requires_one_of if d in all_products]
                if dep_prods:
                    dep_prods.sort(key=lambda p: p.price_min)
                    cheapest = dep_prods[0]
                    active_ids.add(cheapest.product_id)
                    if cheapest.product_id in line_map:
                        line_map[cheapest.product_id]["active"] = True
                    else:
                        line_map[cheapest.product_id] = {
                            "product_id": cheapest.product_id,
                            "category": cheapest.category,
                            "name_plain": cheapest.product_name,
                            "qty": 1,
                            "unit": cheapest.unit,
                            "unit_price": cheapest.price_min,
                            "line_total": cheapest.price_min,
                            "setup_fee": cheapest.setup_fee,
                            "why": f"Prerequisite connection for {prod.product_name}",
                            "min_contract_months": cheapest.min_contract_months,
                            "can_toggle": True,
                            "active": True
                        }
                    auto_added.append(f"{cheapest.product_name} was auto-added as a required prerequisite for {prod.product_name}")

    # 2. Check if toggling off a product broke dependencies for others
    for pid in list(active_ids):
        prod = all_products.get(pid)
        if prod and prod.requires_one_of:
            dep_set = set(prod.requires_one_of)
            if not (dep_set & active_ids):
                line_map[pid]["active"] = False
                active_ids.discard(pid)
                auto_removed.append(f"{prod.product_name} was auto-removed because its prerequisite internet connection was unselected")

    # Re-calculate quote
    active_items = []
    for pid, item in line_map.items():
        if item.get("active", True) and pid in all_products:
            active_items.append({
                "product": all_products[pid],
                "qty": item.get("qty", 1),
                "why": item.get("why", ""),
                "can_toggle": item.get("can_toggle", True)
            })

    quote_calc = calculate_quote(
        active_items=active_items,
        term_months=term_months,
        current_spend=journey.current_spend
    )

    quote_obj.bundle_json = json.dumps(quote_calc["bundle"])
    quote_obj.term_months = term_months
    quote_obj.monthly_total = quote_calc["monthly_recurring"]
    quote_obj.setup_total = quote_calc["one_time_setup"]
    quote_obj.gst_amount = quote_calc["gst_amount"]
    quote_obj.first_invoice_total = quote_calc["first_invoice"]
    quote_obj.tco_term = quote_calc["tco_term"]
    session.add(quote_obj)
    session.commit()

    # Eligibility validation
    ctx = {
        "city_tier": journey.city_tier or "tier_1",
        "employees": journey.employees or 1,
        "sites": journey.sites or 1,
        "has_active_gstin": bool(journey.identifier_type == "gstin" and journey.identifier_raw)
    }
    violations_dict = validate_bundle([it["product"] for it in active_items], ctx)
    violations_list = [f"{pid}: {', '.join(reasons)}" for pid, reasons in violations_dict.items()]

    bundle_pydantic = [BundleLineItem(**b) for b in quote_calc["bundle"]]

    quote_resp = QuoteResponse(
        quote_id=quote_obj.id,
        term_months=term_months,
        monthly_recurring=quote_calc["monthly_recurring"],
        one_time_setup=quote_calc["one_time_setup"],
        gst_amount=quote_calc["gst_amount"],
        first_invoice=quote_calc["first_invoice"],
        tco_term=quote_calc["tco_term"],
        vs_current_spend=quote_calc["vs_current_spend"],
        promised_date=quote_calc["promised_date"],
        bundle=bundle_pydantic,
        excluded=[]
    )

    return QuoteUpdateResponse(
        quote=quote_resp,
        violations=violations_list,
        auto_added=auto_added,
        auto_removed=auto_removed
    )


@router.post("/accept", response_model=QuoteAcceptResponse)
def accept_quote(req: QuoteAcceptRequest, session: Session = Depends(get_session)):
    journey = session.get(Journey, req.journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    quote_obj = session.exec(select(Quote).where(Quote.journey_id == journey.id)).first()
    if not quote_obj:
        raise HTTPException(status_code=404, detail="Quote not found")

    quote_obj.accepted_at = datetime.utcnow().isoformat()
    journey.stage = "CONSENT"
    session.add(quote_obj)
    session.add(journey)

    evt = AppEvent(event_name="quote_accepted", journey_id=journey.id)
    session.add(evt)
    session.commit()

    return QuoteAcceptResponse(quote_id=quote_obj.id)
