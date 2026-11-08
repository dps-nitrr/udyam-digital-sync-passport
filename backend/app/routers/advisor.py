import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.models import Journey, Quote, Product, AppEvent
from backend.app.schemas import (
    AdvisorMessageRequest,
    AdvisorMessageResponse,
    RecommendResponse,
    QuoteResponse,
    BundleLineItem,
    ExcludedProduct
)
from backend.app.services.advisor import process_advisor_message
from backend.app.services.bundles import generate_recommended_bundle
from backend.app.services.pricing import calculate_quote
from backend.app.services.eligibility import check_product_eligibility

router = APIRouter(prefix="/api/advisor", tags=["Advisor"])

@router.post("/message", response_model=AdvisorMessageResponse)
def advisor_message(req: AdvisorMessageRequest, session: Session = Depends(get_session)):
    journey = session.get(Journey, req.journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    res = process_advisor_message(
        journey=journey,
        slot=req.slot,
        chip_value=req.chip_value,
        text=req.text,
        session=session
    )
    
    evt = AppEvent(
        event_name="question_answered",
        journey_id=journey.id,
        payload_json=json.dumps({"state": res["next_state"], "slots": res["slots_filled"]})
    )
    session.add(evt)
    session.commit()

    return AdvisorMessageResponse(**res)


@router.post("/recommend", response_model=RecommendResponse)
def advisor_recommend(req: AdvisorMessageRequest, session: Session = Depends(get_session)):
    journey = session.get(Journey, req.journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    segment = journey.segment
    if journey.sites and journey.sites >= 2:
        segment = "Small multi-site businesses"
    elif not segment:
        segment = "Micro retail & services"
    employees = journey.employees or 1
    sites = journey.sites or 1
    city_tier = journey.city_tier or "tier_1"
    
    # Check if active GSTIN
    has_active_gstin = False
    if journey.identifier_type == "gstin" and journey.identifier_raw:
        from backend.app.models import RegistryGSTIN
        reg = session.get(RegistryGSTIN, journey.identifier_raw)
        if reg and reg.status.lower() == "active":
            has_active_gstin = True

    active_items, excluded_items, default_term = generate_recommended_bundle(
        segment=segment,
        employees=employees,
        sites=sites,
        city_tier=city_tier,
        has_active_gstin=has_active_gstin,
        session=session
    )

    quote_calc = calculate_quote(
        active_items=active_items,
        term_months=default_term,
        current_spend=journey.current_spend
    )

    # Persist or update quote
    existing_quote = session.exec(select(Quote).where(Quote.journey_id == journey.id)).first()
    if not existing_quote:
        quote_obj = Quote(
            journey_id=journey.id,
            bundle_json=json.dumps(quote_calc["bundle"]),
            term_months=default_term,
            monthly_total=quote_calc["monthly_recurring"],
            setup_total=quote_calc["one_time_setup"],
            gst_amount=quote_calc["gst_amount"],
            first_invoice_total=quote_calc["first_invoice"],
            tco_term=quote_calc["tco_term"]
        )
        session.add(quote_obj)
        session.commit()
        session.refresh(quote_obj)
        quote_id = quote_obj.id
    else:
        existing_quote.bundle_json = json.dumps(quote_calc["bundle"])
        existing_quote.term_months = default_term
        existing_quote.monthly_total = quote_calc["monthly_recurring"]
        existing_quote.setup_total = quote_calc["one_time_setup"]
        existing_quote.gst_amount = quote_calc["gst_amount"]
        existing_quote.first_invoice_total = quote_calc["first_invoice"]
        existing_quote.tco_term = quote_calc["tco_term"]
        session.add(existing_quote)
        session.commit()
        quote_id = existing_quote.id

    quote_calc["quote_id"] = quote_id
    quote_calc["excluded"] = excluded_items

    bundle_pydantic = [BundleLineItem(**b) for b in quote_calc["bundle"]]
    excluded_pydantic = [ExcludedProduct(**ex) for ex in excluded_items]

    quote_resp = QuoteResponse(
        quote_id=quote_id,
        term_months=quote_calc["term_months"],
        monthly_recurring=quote_calc["monthly_recurring"],
        one_time_setup=quote_calc["one_time_setup"],
        gst_amount=quote_calc["gst_amount"],
        first_invoice=quote_calc["first_invoice"],
        tco_term=quote_calc["tco_term"],
        vs_current_spend=quote_calc["vs_current_spend"],
        promised_date=quote_calc["promised_date"],
        bundle=bundle_pydantic,
        excluded=excluded_pydantic
    )

    return RecommendResponse(
        bundle=bundle_pydantic,
        excluded=excluded_pydantic,
        quote=quote_resp
    )
