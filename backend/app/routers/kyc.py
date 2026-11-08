import os
import json
import hashlib
import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.config import settings
from backend.app.models import Journey, KycCheck, AppEvent
from backend.app.schemas import (
    KycUploadResponse,
    CheckItem,
    KycFinalizeRequest,
    KycFinalizeResponse
)
from backend.app.services.kyc import run_11_kyc_checks
from backend.app.services.kyc_fixtures_data import FIXTURES_DATA
from backend.app.services.privacy import mask_identifier

router = APIRouter(prefix="/api/kyc", tags=["KYC"])

DOC_NAMES = {
    "gst_cert": "GST Certificate",
    "udyam_cert": "Udyam Registration Certificate",
    "signatory_id": "Authorised Signatory ID",
    "address_proof": "Address Proof (Electricity Bill)"
}

@router.post("/upload", response_model=KycUploadResponse)
async def upload_kyc_document(
    journey_id: str = Form(...),
    doc_type: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB size limit")

    sha256_hash = hashlib.sha256(content).hexdigest()

    # Determine extracted fields
    # If the filename or content matches a fixture, load fixture data; else default structure
    fn = file.filename or ""
    fixture_key = "K03"  # default clean pass
    for kid in FIXTURES_DATA.keys():
        if kid in fn or kid.lower() in fn.lower():
            fixture_key = kid
            break

    # If applicant has a specific GSTIN in journey, match fixture
    if journey.identifier_raw:
        for kid, f_data in FIXTURES_DATA.items():
            if f_data.get("gst_cert", {}).get("gstin") == journey.identifier_raw:
                fixture_key = kid
                break

    extracted = dict(FIXTURES_DATA[fixture_key].get(doc_type, {}))

    # Mask sensitive fields
    masked_extracted = dict(extracted)
    if "gstin" in masked_extracted:
        masked_extracted["gstin"] = mask_identifier(masked_extracted["gstin"])
    if "udyam_number" in masked_extracted:
        masked_extracted["udyam_number"] = mask_identifier(masked_extracted["udyam_number"])
    if "id_no" in masked_extracted:
        masked_extracted["id_no"] = mask_identifier(masked_extracted["id_no"])
    if "consumer_no" in masked_extracted:
        masked_extracted["consumer_no"] = mask_identifier(masked_extracted["consumer_no"])

    # Run check for this document
    all_docs = {doc_type: extracted}
    verdict, checks = run_11_kyc_checks(all_docs, session)

    # Filter checks relevant to this document
    relevant_checks = []
    for c in checks:
        cid = c["id"]
        if doc_type == "gst_cert" and cid in ["chk_1", "chk_2", "chk_3"]:
            relevant_checks.append(c)
        elif doc_type == "udyam_cert" and cid in ["chk_4"]:
            relevant_checks.append(c)
        elif doc_type == "signatory_id" and cid in ["chk_9", "chk_10"]:
            relevant_checks.append(c)
        elif doc_type == "address_proof" and cid in ["chk_7", "chk_8"]:
            relevant_checks.append(c)
    if not relevant_checks:
        relevant_checks = checks[:2]

    # Save check record to database
    existing_check = session.exec(
        select(KycCheck).where(KycCheck.journey_id == journey.id, KycCheck.doc_type == doc_type)
    ).first()

    if not existing_check:
        check_record = KycCheck(
            journey_id=journey.id,
            doc_type=doc_type,
            extracted_json=json.dumps(extracted),
            checks_json=json.dumps(relevant_checks),
            verdict=verdict,
            image_sha256=sha256_hash
        )
        session.add(check_record)
    else:
        existing_check.extracted_json = json.dumps(extracted)
        existing_check.checks_json = json.dumps(relevant_checks)
        existing_check.verdict = verdict
        existing_check.image_sha256 = sha256_hash
        session.add(existing_check)

    session.commit()

    return KycUploadResponse(
        doc_type=doc_type,
        extracted=masked_extracted,
        checks=[CheckItem(**c) for c in relevant_checks],
        verdict=verdict,
        message=f"{DOC_NAMES.get(doc_type, doc_type)} processed successfully."
    )


@router.post("/finalize", response_model=KycFinalizeResponse)
def finalize_kyc(req: KycFinalizeRequest, session: Session = Depends(get_session)):
    journey = session.get(Journey, req.journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    checks_records = session.exec(
        select(KycCheck).where(KycCheck.journey_id == journey.id)
    ).all()

    uploaded_docs = {}
    for r in checks_records:
        uploaded_docs[r.doc_type] = json.loads(r.extracted_json)

    # Check required documents
    required_docs = ["gst_cert", "address_proof", "signatory_id"]
    missing = [DOC_NAMES[d] for d in required_docs if d not in uploaded_docs]

    # If missing documents, mark review/incomplete
    if missing:
        return KycFinalizeResponse(
            overall_verdict="review",
            missing=missing,
            next_action="Upload the remaining required documents to complete instant verification.",
            details=[]
        )

    verdict, checks = run_11_kyc_checks(uploaded_docs, session)

    if verdict == "pass":
        journey.stage = "TRACKER"
        next_action = "All 11 checks verified. Ready to activate instant order dispatch."
    elif verdict == "review":
        next_action = "Assigned to fulfillment desk for priority 1-hour verification review."
    else:
        next_action = "Verification issue detected. Please review the highlighted document check above."

    session.add(journey)
    session.commit()

    return KycFinalizeResponse(
        overall_verdict=verdict,
        missing=[],
        next_action=next_action,
        details=checks
    )


@router.post("/load-specimen")
def load_specimen_fixture(payload: dict, session: Session = Depends(get_session)):
    journey_id = payload.get("journey_id")
    fixture_id = payload.get("fixture_id", "K03").upper()
    
    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")
        
    f_data = FIXTURES_DATA.get(fixture_id, FIXTURES_DATA["K03"])
    
    # Clear any previous checks for this journey
    old_checks = session.exec(select(KycCheck).where(KycCheck.journey_id == journey.id)).all()
    for c in old_checks:
        session.delete(c)
    session.commit()
    
    # Add each doc
    for doc_type, fields in f_data.items():
        kyc_record = KycCheck(
            journey_id=journey.id,
            doc_type=doc_type,
            extracted_json=json.dumps(fields),
            checks_json=json.dumps([]),
            verdict="pass",
            image_sha256=hashlib.sha256(f"{journey.id}_{fixture_id}_{doc_type}".encode()).hexdigest()
        )
        session.add(kyc_record)
    session.commit()
    
    verdict, checks = run_11_kyc_checks(f_data, session)
    if verdict == "pass":
        next_action = "All 11 checks verified. Ready to activate instant order dispatch."
    elif verdict == "review":
        next_action = "Assigned to fulfillment desk for priority 1-hour verification review."
    else:
        next_action = "Verification issue detected. Please review the highlighted document check above."
        
    return {
        "fixture_id": fixture_id,
        "overall_verdict": verdict,
        "docs_loaded": list(f_data.keys()),
        "extracted_data": f_data,
        "next_action": next_action,
        "checks": checks
    }

