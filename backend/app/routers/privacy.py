import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.models import Journey, Consent, KycCheck, Order, Quote, Notification

router = APIRouter(prefix="/api/privacy", tags=["DPDP Privacy Rights"])

@router.get("/export/{journey_id}")
def export_user_data(journey_id: str, session: Session = Depends(get_session)):
    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    consent = session.exec(select(Consent).where(Consent.journey_id == journey.id)).all()
    kyc_records = session.exec(select(KycCheck).where(KycCheck.journey_id == journey.id)).all()
    quotes = session.exec(select(Quote).where(Quote.journey_id == journey.id)).all()
    orders = session.exec(select(Order).where(Order.journey_id == journey.id)).all()

    return {
        "export_date": "2026-07-15T10:00:00Z",
        "regime": "Digital Personal Data Protection (DPDP) Act 2023",
        "journey": {
            "id": journey.id,
            "business_name": journey.business_name,
            "identifier_type": journey.identifier_type,
            "identifier_masked": journey.identifier_masked,
            "language": journey.language,
            "segment": journey.segment,
            "employees": journey.employees,
            "sites": journey.sites,
            "stage": journey.stage
        },
        "consents": [
            {
                "id": c.id,
                "purposes": json.loads(c.purposes_json),
                "granted_at": c.granted_at,
                "hash": c.hash
            } for c in consent
        ],
        "kyc_checks": [
            {
                "doc_type": k.doc_type,
                "verdict": k.verdict,
                "image_sha256": k.image_sha256
            } for k in kyc_records
        ],
        "quotes": [
            {
                "monthly_total": q.monthly_total,
                "term_months": q.term_months,
                "created_at": q.created_at
            } for q in quotes
        ],
        "orders": [
            {
                "status": o.status,
                "promised_date": o.promised_date
            } for o in orders
        ]
    }


@router.delete("/{journey_id}")
def erase_user_data(journey_id: str, session: Session = Depends(get_session)):
    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    # Erase associated data per DPDP right to erasure
    for c in session.exec(select(Consent).where(Consent.journey_id == journey.id)).all():
        session.delete(c)
    for k in session.exec(select(KycCheck).where(KycCheck.journey_id == journey.id)).all():
        session.delete(k)
    for q in session.exec(select(Quote).where(Quote.journey_id == journey.id)).all():
        session.delete(q)
    for o in session.exec(select(Order).where(Order.journey_id == journey.id)).all():
        session.delete(o)

    session.delete(journey)
    session.commit()

    return {
        "status": "success",
        "message": f"All personal data and records for journey {journey_id} have been permanently erased from active stores."
    }
