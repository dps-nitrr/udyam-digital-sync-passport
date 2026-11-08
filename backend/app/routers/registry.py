from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.models import Journey, AppEvent
from backend.app.schemas import (
    JourneyCreateRequest,
    JourneyCreateResponse,
    RegistryLookupRequest,
    RegistryLookupResponse,
    BusinessDetails,
    SegmentGuess
)
from backend.app.services.gstin import (
    normalize_gstin,
    check_gstin_format,
    lookup_gstin
)
from backend.app.services.udyam import (
    normalize_udyam,
    check_udyam_format,
    lookup_udyam
)
from backend.app.services.segments import infer_segment
from backend.app.services.privacy import mask_identifier

router = APIRouter(prefix="/api", tags=["Registry & Journey"])

@router.post("/journeys", response_model=JourneyCreateResponse)
def create_journey(req: JourneyCreateRequest, session: Session = Depends(get_session)):
    journey = Journey(
        language=req.language,
        source=req.source or "self"
    )
    session.add(journey)
    session.commit()
    session.refresh(journey)

    evt = AppEvent(event_name="journey_started", journey_id=journey.id)
    session.add(evt)
    session.commit()

    return JourneyCreateResponse(journey_id=journey.id)


@router.post("/registry/lookup", response_model=RegistryLookupResponse)
def lookup_identifier(req: RegistryLookupRequest, session: Session = Depends(get_session)):
    raw = req.identifier.strip()
    
    # Auto-detect identifier type
    is_udyam = raw.upper().startswith("UDYAM") or "-" in raw
    
    journey = session.get(Journey, req.journey_id) if req.journey_id else None

    if is_udyam:
        ident_type = "udyam"
        res = lookup_udyam(raw, session)
        valid = res["valid_format"]
        found = res["found"]
        status = "Active" if found else None
        
        bus_details = None
        seg_guess = None
        if found:
            bus_details = BusinessDetails(
                name=res["enterprise_name"],
                trade_name=res["enterprise_name"],
                legal_name=res["enterprise_name"],
                address=f"{res['city']}, {res['state']}",
                state=res["state"],
                city=res["city"],
                status="Active",
                enterprise_type=res["enterprise_type"],
                nic_description=res["nic_description"]
            )
            inferred = infer_segment(
                trade_name=res["enterprise_name"],
                nic_description=res["nic_description"],
                enterprise_type=res["enterprise_type"],
                major_activity=res["major_activity"]
            )
            seg_guess = SegmentGuess(
                segment=inferred["segment"],
                confidence=inferred["confidence"],
                reason_key=inferred["reason_key"],
                reason_display=inferred["reason_display"]
            )

        if journey:
            journey.identifier_type = "udyam"
            journey.identifier_raw = raw
            journey.identifier_masked = mask_identifier(raw)
            if bus_details:
                journey.business_name = bus_details.name
                journey.state = bus_details.state
                journey.city = bus_details.city
            if seg_guess:
                journey.segment = seg_guess.segment
            session.add(journey)
            session.commit()

        return RegistryLookupResponse(
            identifier_type="udyam",
            valid_format=valid,
            checksum_ok=valid,
            found=found,
            status=status,
            business=bus_details,
            segment_guess=seg_guess,
            suggestion=None,
            gst_status_issue=False
        )

    else:
        # GSTIN lookup
        ident_type = "gstin"
        res = lookup_gstin(raw, session)
        
        bus_details = None
        seg_guess = None
        if res["found"]:
            bus_details = BusinessDetails(
                name=res["trade_name"] or res["legal_name"],
                legal_name=res["legal_name"],
                trade_name=res["trade_name"],
                address=res["address"],
                state=res["state"],
                constitution=res["constitution"],
                status=res["status"]
            )
            inferred = infer_segment(
                trade_name=res["trade_name"],
                legal_name=res["legal_name"]
            )
            seg_guess = SegmentGuess(
                segment=inferred["segment"],
                confidence=inferred["confidence"],
                reason_key=inferred["reason_key"],
                reason_display=inferred["reason_display"]
            )

        if journey:
            journey.identifier_type = "gstin"
            journey.identifier_raw = raw
            journey.identifier_masked = mask_identifier(raw)
            if bus_details:
                journey.business_name = bus_details.name
                journey.trade_name = bus_details.trade_name
                journey.legal_name = bus_details.legal_name
                journey.state = bus_details.state
                journey.address = bus_details.address
                journey.constitution = bus_details.constitution
            if seg_guess:
                journey.segment = seg_guess.segment
            session.add(journey)
            session.commit()

        return RegistryLookupResponse(
            identifier_type="gstin",
            valid_format=res["valid_format"],
            checksum_ok=res["checksum_ok"],
            found=res["found"],
            status=res["status"],
            business=bus_details,
            segment_guess=seg_guess,
            suggestion=res.get("suggestion"),
            gst_status_issue=res["gst_status_issue"]
        )
