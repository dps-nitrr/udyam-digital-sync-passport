from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.models import Lead, Journey, Partner
from backend.app.schemas import BackofficeLeadItem, AssignLeadRequest
from backend.app.services.propensity import score_lead

router = APIRouter(prefix="/api/backoffice", tags=["Backoffice"])

# In-memory assignment map for demo
ASSIGNMENTS = {}

@router.get("/leads", response_model=List[BackofficeLeadItem])
def list_backoffice_leads(
    segment: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    score_min: Optional[int] = Query(0),
    session: Session = Depends(get_session)
):
    results: List[BackofficeLeadItem] = []

    # 1. Include live journeys first (real-time dropped/in-progress leads)
    journeys = session.exec(select(Journey).order_by(Journey.created_at.desc())).all()
    for j in journeys:
        data = {
            "segment": j.segment,
            "business_type": j.trade_name or j.business_name,
            "city_tier": j.city_tier,
            "lead_source": j.source,
            "preferred_language": j.language,
            "annual_turnover_band": "10L - 50L",
            "has_gstin": "Y" if j.identifier_type == "gstin" else "N",
            "has_udyam": "Y" if j.identifier_type == "udyam" else "N",
            "current_internet": "Broadband",
            "employee_count": j.employees,
            "num_sites": j.sites,
            "monthly_telecom_spend_inr": j.current_spend or 3000,
            "stage_reached": j.stage,
            "drop_reason": j.handoff_reason
        }
        score, factors, rec_action = score_lead(data)
        
        assigned = ASSIGNMENTS.get(j.id, "Unassigned")
        if j.source.startswith("partner:"):
            assigned = j.source.split("partner:")[-1]

        item = BackofficeLeadItem(
            lead_or_journey_id=j.id[:8].upper(),
            source_type="journey",
            business_name=j.business_name or "New Inbound Prospect",
            segment=j.segment or "Micro retail & services",
            stage_reached=j.stage,
            score=score,
            top_factors=factors,
            recommended_action=rec_action,
            drop_reason=j.handoff_reason or ("In Progress" if j.stage != "TRACKER" else "Active"),
            assigned_partner=assigned,
            source=j.source,
            phone=j.phone or "+91 98XXX XXXXX"
        )
        results.append(item)

    # 2. Add sample seed leads from smb_leads
    stmt = select(Lead)
    if segment:
        stmt = stmt.where(Lead.segment == segment)
    if stage:
        stmt = stmt.where(Lead.stage_reached == stage)
        
    leads = session.exec(stmt.limit(40)).all()
    for l in leads:
        lead_dict = {
            "segment": l.segment,
            "business_type": l.business_type,
            "city_tier": l.city_tier,
            "lead_source": l.lead_source,
            "preferred_language": l.preferred_language,
            "annual_turnover_band": l.annual_turnover_band,
            "has_gstin": l.has_gstin,
            "has_udyam": l.has_udyam,
            "current_internet": l.current_internet,
            "employee_count": l.employee_count,
            "num_sites": l.num_sites,
            "monthly_telecom_spend_inr": l.monthly_telecom_spend_inr,
            "products_of_interest": l.products_of_interest,
            "stage_reached": l.stage_reached,
            "drop_reason": l.drop_reason
        }
        score, factors, rec_action = score_lead(lead_dict)
        
        assigned = ASSIGNMENTS.get(l.lead_id, "Field Desk")

        item = BackofficeLeadItem(
            lead_or_journey_id=l.lead_id,
            source_type="lead",
            business_name=l.business_name or "SMB Customer",
            segment=l.segment or "Micro retail & services",
            stage_reached=l.stage_reached or "Contacted",
            score=score,
            top_factors=factors,
            recommended_action=rec_action,
            drop_reason=l.drop_reason or ("Activated" if l.outcome == "Activated" else None),
            assigned_partner=assigned,
            source=l.lead_source or "Field sales",
            phone="+91 99XXX XXXXX"
        )
        results.append(item)

    # Filter by score_min
    if score_min and score_min > 0:
        results = [r for r in results if r.score >= score_min]

    # Sort high propensity first
    results.sort(key=lambda r: r.score, reverse=True)
    return results


@router.post("/leads/{lead_id}/assign")
def assign_lead(lead_id: str, req: AssignLeadRequest):
    ASSIGNMENTS[lead_id] = req.partner_id
    return {"ok": True, "lead_id": lead_id, "assigned_to": req.partner_id}
