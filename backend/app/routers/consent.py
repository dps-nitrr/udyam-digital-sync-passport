import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.models import Journey, Consent, AppEvent
from backend.app.schemas import (
    ConsentNoticeResponse,
    PurposeItem,
    ConsentGrantRequest,
    ConsentGrantResponse
)
from backend.app.services.privacy import compute_hash_chain

router = APIRouter(prefix="/api/consent", tags=["Consent"])

PURPOSES_DEF = {
    "en": [
        PurposeItem(
            id="verify_identity",
            text="Verify business registration & tax identity (GST / Udyam)",
            required=True,
            description="Used strictly to cross-reference registered business entity credentials with government portals."
        ),
        PurposeItem(
            id="verify_address",
            text="Verify business installation premises",
            required=True,
            description="Used to confirm physical feasibility and service installation address."
        ),
        PurposeItem(
            id="verify_signatory",
            text="Verify legal signatory authorization",
            required=True,
            description="Ensures the applicant has authorized contracting authority on behalf of the enterprise."
        ),
        PurposeItem(
            id="order_updates",
            text="Real-time order tracker updates on WhatsApp & SMS",
            required=False,
            description="Simulated dispatch alerts and technician appointment scheduling."
        ),
        PurposeItem(
            id="product_offers",
            text="Future customized enterprise connectivity offers",
            required=False,
            description="Optional recommendations for speed upgrades and seasonal business discounts."
        )
    ],
    "hi": [
        PurposeItem(
            id="verify_identity",
            text="व्यावसायिक पंजीकरण और कर पहचान (GST / उद्यम) का सत्यापन",
            required=True,
            description="सरकारी रिकॉर्ड के साथ व्यावसायिक इकाई के सत्यापन के लिए आवश्यक।"
        ),
        PurposeItem(
            id="verify_address",
            text="स्थापना पते (Installation Address) का सत्यापन",
            required=True,
            description="कनेक्शन लगाने के स्थान की पुष्टि के लिए आवश्यक।"
        ),
        PurposeItem(
            id="verify_signatory",
            text="हस्ताक्षरकर्ता (Signatory) के कानूनी अधिकार का सत्यापन",
            required=True,
            description="यह सुनिश्चित करने के लिए कि आवेदक व्यवसाय की ओर से अनुबंध करने के लिए अधिकृत है।"
        ),
        PurposeItem(
            id="order_updates",
            text="व्हाट्सएप और एसएमएस पर लाइव ऑर्डर ट्रैकर अपडेट",
            required=False,
            description="तकनीशियन के आने और इंस्टॉलेशन की रीयल-टाइम सूचना।"
        ),
        PurposeItem(
            id="product_offers",
            text="भविष्य के विशेष व्यावसायिक कनेक्टिविटी ऑफ़र",
            required=False,
            description="गति बढ़ाने और विशेष छूट के ऐच्छिक सुझाव।"
        )
    ]
}

@router.get("/notice", response_model=ConsentNoticeResponse)
def get_consent_notice(lang: str = Query("en")):
    purposes = PURPOSES_DEF.get(lang, PURPOSES_DEF["en"])
    retention_text = (
        "Document images are purged immediately post-verification (max 30 min). Minimised extracted metadata is stored strictly for the contract audit trail."
        if lang == "en" else
        "दस्तावेज़ की तस्वीरें सत्यापन के तुरंत बाद (अधिकतम 30 मिनट में) हटा दी जाती हैं। केवल न्यूनतम ऑडिट डेटा सुरक्षित रखा जाता है।"
    )
    rights_text = (
        "Under DPDP Act 2023, you have the right to access, export, or withdraw consent and request data erasure anytime under 'My Data'."
        if lang == "en" else
        "डीपीडीपी अधिनियम के तहत, आपको कभी भी 'मेरा डेटा' के अंतर्गत सहमति वापस लेने या डेटा मिटाने का पूरा अधिकार है।"
    )
    return ConsentNoticeResponse(
        version="1.0",
        purposes=purposes,
        retention=retention_text,
        rights=rights_text
    )


@router.post("", response_model=ConsentGrantResponse)
def grant_consent(req: ConsentGrantRequest, session: Session = Depends(get_session)):
    journey = session.get(Journey, req.journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    # Find latest consent row to maintain hash chain
    last_consent = session.exec(
        select(Consent).order_by(Consent.granted_at.desc())
    ).first()

    prev_hash = last_consent.hash if last_consent else "GENESIS_CONSENT_CHAIN_0000000000000000"
    
    payload = {
        "journey_id": journey.id,
        "accepted_purposes": req.accepted_purposes,
        "notice_version": "1.0",
        "language": journey.language
    }
    cur_hash = compute_hash_chain(prev_hash, payload)

    consent_entry = Consent(
        journey_id=journey.id,
        purposes_json=json.dumps(req.accepted_purposes),
        notice_version="1.0",
        language=journey.language,
        prev_hash=prev_hash,
        hash=cur_hash
    )
    session.add(consent_entry)
    
    journey.stage = "KYC"
    session.add(journey)

    evt = AppEvent(event_name="consent_granted", journey_id=journey.id)
    session.add(evt)
    session.commit()
    session.refresh(consent_entry)

    return ConsentGrantResponse(
        consent_id=consent_entry.id,
        receipt_url=f"/api/consent/receipt/{consent_entry.id}",
        hash=cur_hash
    )
