from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Journey
class JourneyCreateRequest(BaseModel):
    language: str = "en"
    source: Optional[str] = "self"

class JourneyCreateResponse(BaseModel):
    journey_id: str

# Registry
class RegistryLookupRequest(BaseModel):
    identifier: str
    journey_id: Optional[str] = None

class BusinessDetails(BaseModel):
    name: str
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    address: str
    state: str
    city: Optional[str] = None
    constitution: Optional[str] = None
    status: Optional[str] = None
    enterprise_type: Optional[str] = None
    nic_description: Optional[str] = None

class SegmentGuess(BaseModel):
    segment: str
    confidence: float
    reason_key: str
    reason_display: str

class RegistryLookupResponse(BaseModel):
    identifier_type: str  # gstin | udyam | unknown
    valid_format: bool
    checksum_ok: bool
    found: bool
    status: Optional[str] = None
    business: Optional[BusinessDetails] = None
    segment_guess: Optional[SegmentGuess] = None
    suggestion: Optional[str] = None
    gst_status_issue: bool = False

# Advisor
class AdvisorMessageRequest(BaseModel):
    journey_id: str
    slot: Optional[str] = None
    chip_value: Optional[Any] = None
    text: Optional[str] = None

class ChipOption(BaseModel):
    label: str
    value: Any

class AdvisorMessageResponse(BaseModel):
    next_state: str
    assistant_message: str
    chips: Optional[List[ChipOption]] = None
    slots_filled: Dict[str, Any]
    handoff: bool = False
    handoff_reason: Optional[str] = None
    llm_used: bool = False

# Quote & Bundle
class BundleLineItem(BaseModel):
    product_id: str
    category: str
    name_plain: str
    qty: int
    unit: str
    unit_price: int
    line_total: int
    setup_fee: int
    why: str
    min_contract_months: int
    can_toggle: bool = True
    active: bool = True

class ExcludedProduct(BaseModel):
    product_id: str
    product_name: str
    reason_key: str
    reason_plain: str

class QuoteResponse(BaseModel):
    quote_id: Optional[str] = None
    term_months: int
    monthly_recurring: int
    one_time_setup: int
    gst_amount: int
    first_invoice: int
    tco_term: int
    vs_current_spend: Optional[float] = None
    promised_date: str
    bundle: List[BundleLineItem]
    excluded: List[ExcludedProduct]

class RecommendResponse(BaseModel):
    bundle: List[BundleLineItem]
    excluded: List[ExcludedProduct]
    quote: QuoteResponse

class QuoteUpdateRequest(BaseModel):
    journey_id: str
    term_months: Optional[int] = None
    toggles: Optional[Dict[str, bool]] = None
    quantities: Optional[Dict[str, int]] = None

class QuoteUpdateResponse(BaseModel):
    quote: QuoteResponse
    violations: List[str]
    auto_added: List[str]
    auto_removed: List[str]

class QuoteAcceptRequest(BaseModel):
    journey_id: str

class QuoteAcceptResponse(BaseModel):
    quote_id: str

# Consent
class PurposeItem(BaseModel):
    id: str
    text: str
    required: bool
    description: str

class ConsentNoticeResponse(BaseModel):
    version: str
    purposes: List[PurposeItem]
    retention: str
    rights: str

class ConsentGrantRequest(BaseModel):
    journey_id: str
    accepted_purposes: List[str]

class ConsentGrantResponse(BaseModel):
    consent_id: str
    receipt_url: str
    hash: str

# KYC
class CheckItem(BaseModel):
    id: str
    label: str
    status: str  # pass | review | fail
    detail: str

class KycUploadResponse(BaseModel):
    doc_type: str
    extracted: Dict[str, Any]
    checks: List[CheckItem]
    verdict: str  # pass | review | fail
    message: str

class KycFinalizeRequest(BaseModel):
    journey_id: str

class KycFinalizeResponse(BaseModel):
    overall_verdict: str  # pass | review | fail
    missing: List[str]
    next_action: str
    details: List[Dict[str, Any]]

# Auth OTP
class OtpRequest(BaseModel):
    phone: str

class OtpVerifyRequest(BaseModel):
    phone: Optional[str] = "9876543210"
    code: str

class OtpVerifyResponse(BaseModel):
    valid: bool
    token: str

# Orders & Tracker
class TimelineItem(BaseModel):
    status_key: str
    label: str
    done: bool
    current: bool
    ts: Optional[str] = None
    eta: str

class NotificationItem(BaseModel):
    id: str
    channel: str
    body: str
    language: str
    ts: str

class OrderStatusResponse(BaseModel):
    order_id: str
    journey_id: str
    status: str
    promised_date: str
    timeline: List[TimelineItem]
    notifications: List[NotificationItem]

class OrderSimulateRequest(BaseModel):
    days: Optional[int] = 1

# Backoffice
class BackofficeLeadItem(BaseModel):
    lead_or_journey_id: str
    source_type: str  # lead | journey
    business_name: str
    segment: str
    stage_reached: str
    score: int
    top_factors: List[str]
    recommended_action: str
    drop_reason: Optional[str] = None
    assigned_partner: Optional[str] = None
    source: str
    phone: Optional[str] = None

class AssignLeadRequest(BaseModel):
    partner_id: str

class FunnelMetric(BaseModel):
    stage: str
    count: int
    conversion_pct: float

class DropReasonMetric(BaseModel):
    reason: str
    count: int
    digital_fixable: bool

class DashboardKPIs(BaseModel):
    total_leads: int
    lead_to_activation_pct: float
    avg_days_to_activation: float
    chase_calls_per_customer: float
    cost_per_activation_inr: float
    funnel: List[FunnelMetric]
    drop_reasons: List[DropReasonMetric]
    digital_fixable_pct: float
