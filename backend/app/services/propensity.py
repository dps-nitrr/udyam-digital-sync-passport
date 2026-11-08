import os
import joblib
import pandas as pd
from typing import Dict, Any, List, Tuple
from pathlib import Path
from backend.app.config import settings

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = ROOT_DIR / "models" / "propensity.joblib"

_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None and MODEL_PATH.exists():
        _pipeline = joblib.load(MODEL_PATH)
    return _pipeline

def score_lead(data: Dict[str, Any]) -> Tuple[int, List[str], str]:
    """
    Computes propensity score (0-100), top factors, and recommended action.
    """
    pipeline = get_pipeline()
    
    products_interest = str(data.get("products_of_interest") or "")
    num_products = len([x for x in products_interest.split(";") if x.strip()])
    
    features = pd.DataFrame([{
        "segment": str(data.get("segment") or "Missing"),
        "business_type": str(data.get("business_type") or "Missing"),
        "city_tier": str(data.get("city_tier") or "Missing"),
        "lead_source": str(data.get("lead_source") or "Missing"),
        "preferred_language": str(data.get("preferred_language") or "Missing"),
        "annual_turnover_band": str(data.get("annual_turnover_band") or "Missing"),
        "has_gstin": str(data.get("has_gstin") or "Missing"),
        "has_udyam": str(data.get("has_udyam") or "Missing"),
        "current_internet": str(data.get("current_internet") or "Missing"),
        "employee_count": float(data.get("employee_count") or 1),
        "num_sites": float(data.get("num_sites") or 1),
        "monthly_telecom_spend_inr": float(data.get("monthly_telecom_spend_inr") or 3000),
        "num_products_interest": float(num_products)
    }])

    score = 50
    if pipeline:
        try:
            proba = pipeline.predict_proba(features)[0, 1]
            # Scale probability relative to base rate (~7.4%) to a 0-100 index
            score = int(min(99, max(5, proba * 500)))
        except Exception as e:
            print("Scoring error:", e)

    # Top driving factors
    factors = []
    num_sites = float(data.get("num_sites") or 1)
    spend = float(data.get("monthly_telecom_spend_inr") or 0)
    has_gst = str(data.get("has_gstin") or "N").upper() == "Y"
    seg = str(data.get("segment") or "")

    if num_sites >= 3:
        factors.append("Multi-site presence indicates higher enterprise lifetime value")
    if spend >= 5000:
        factors.append("Above-average current telecom expenditure (budget headroom)")
    if has_gst:
        factors.append("Registered GST enterprise with formal compliance")
    if "Professional" in seg or "Multi-site" in seg:
        factors.append(f"High-propensity business vertical ({seg})")
    if not factors:
        factors.append("Established local business with steady operations")

    # Rule-based recommended action
    stage = str(data.get("stage_reached") or "")
    drop_reason = str(data.get("drop_reason") or "").lower()

    if score >= 60 and "quote" in stage.lower():
        action = "High propensity lead dropped at quote: call within 2h with 24-month price guarantee."
    elif not has_gst and "micro" in seg.lower():
        action = "Micro business without GST: send WhatsApp link for GST-free AirFiber starter."
    elif num_sites >= 3:
        action = "Multi-location enterprise: dispatch field partner for SD-WAN and failover demo."
    elif "kyc" in drop_reason or "document" in drop_reason or "signatory" in drop_reason:
        action = "Stalled at documentation: send delegated WhatsApp signing link directly to business owner."
    elif score >= 50:
        action = "Qualified prospect: field executive to schedule direct in-person consultation."
    else:
        action = "Nurture lead via automated SMS/WhatsApp product updates."

    return score, factors[:3], action
