import pandas as pd
from pathlib import Path
from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend.app.db import get_session
from backend.app.config import settings
from backend.app.schemas import DashboardKPIs, FunnelMetric, DropReasonMetric

router = APIRouter(prefix="/api/metrics", tags=["Metrics & KPIs"])

DIGITAL_FIXABLE_REASONS = {
    # 10 reasons from Section 12
    "Visit not scheduled",
    "Visit cancelled by customer",
    "Quote delayed / too complex",
    "Price / quote dispute",
    "Paperwork / document collection delay",
    "Signatory not available",
    "KYC rejection / doc mismatch",
    "GST / Udyam proof missing",
    "Installation delayed beyond promised date",
    "Digital payment failure / UPI timeout"
}

@router.get("/kpis", response_model=DashboardKPIs)
def get_dashboard_kpis(session: Session = Depends(get_session)):
    csv_path = settings.DATA_DIR / "smb_leads.csv"
    
    total_leads = 5000
    activated_cnt = 368
    avg_days = 17.6
    chase_calls = 3.0
    cost_per_act = 15000.0

    funnel_metrics = [
        FunnelMetric(stage="Lead", count=5000, conversion_pct=100.0),
        FunnelMetric(stage="Contacted", count=3406, conversion_pct=68.1),
        FunnelMetric(stage="Needs assessed", count=1974, conversion_pct=58.0),
        FunnelMetric(stage="Quote accepted", count=861, conversion_pct=43.6),
        FunnelMetric(stage="KYC complete", count=588, conversion_pct=68.3),
        FunnelMetric(stage="Activated", count=368, conversion_pct=62.6)
    ]

    drop_reason_metrics: list[DropReasonMetric] = []
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        dropped = df[df["outcome"] == "Dropped"]
        counts = dropped["drop_reason"].value_counts()
        for reason, count in counts.items():
            is_fixable = any(fix.lower() in str(reason).lower() for fix in DIGITAL_FIXABLE_REASONS)
            drop_reason_metrics.append(
                DropReasonMetric(
                    reason=str(reason),
                    count=int(count),
                    digital_fixable=is_fixable
                )
            )

    fixable_sum = sum(d.count for d in drop_reason_metrics if d.digital_fixable)
    total_drops = sum(d.count for d in drop_reason_metrics) or 1
    fixable_pct = round((fixable_sum / total_drops) * 100, 1)

    return DashboardKPIs(
        total_leads=total_leads,
        lead_to_activation_pct=round((activated_cnt / total_leads) * 100, 2),
        avg_days_to_activation=avg_days,
        chase_calls_per_customer=chase_calls,
        cost_per_activation_inr=cost_per_act,
        funnel=funnel_metrics,
        drop_reasons=drop_reason_metrics[:12],
        digital_fixable_pct=fixable_pct
    )
