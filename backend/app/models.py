import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from sqlmodel import SQLModel, Field

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Product(SQLModel, table=True):
    __tablename__ = "product"
    
    product_id: str = Field(primary_key=True)
    category: str
    product_name: str
    description: str
    unit: str
    price_min: int  # price_min_inr_per_month
    price_max: int  # price_max_inr_per_month
    setup_fee: int  # one_time_setup_inr
    min_contract_months: int
    tiers_json: str = "[]"  # available_city_tiers parsed to json list
    min_employees: int = 1
    min_sites: int = 1
    requires_gstin: bool = False
    requires_one_of_json: str = "[]"  # list of product_ids parsed from |
    install_days: int = 1  # typical_install_days
    target_segments_json: str = "[]"  # list of target segments parsed from ;

    @property
    def tiers(self) -> List[str]:
        return json.loads(self.tiers_json)

    @property
    def requires_one_of(self) -> List[str]:
        return json.loads(self.requires_one_of_json)

    @property
    def target_segments(self) -> List[str]:
        return json.loads(self.target_segments_json)


class RegistryGSTIN(SQLModel, table=True):
    __tablename__ = "registry_gstin"
    
    gstin: str = Field(primary_key=True, index=True)
    legal_name: str
    trade_name: str
    constitution: str
    principal_place_of_business: str
    state: str
    registration_date: str
    status: str  # Active, Cancelled, Suspended


class RegistryUdyam(SQLModel, table=True):
    __tablename__ = "registry_udyam"
    
    udyam_number: str = Field(primary_key=True, index=True)
    enterprise_name: str
    enterprise_type: str  # Micro, Small, Medium
    major_activity: str
    nic_description: str
    state: str
    city: str
    date_of_registration: str


class Lead(SQLModel, table=True):
    __tablename__ = "lead"
    
    lead_id: str = Field(primary_key=True, index=True)
    created_date: Optional[str] = None
    lead_source: Optional[str] = None
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    segment: Optional[str] = None
    city: Optional[str] = None
    city_tier: Optional[str] = None
    state: Optional[str] = None
    preferred_language: Optional[str] = None
    employee_count: Optional[int] = None
    num_sites: Optional[int] = None
    annual_turnover_band: Optional[str] = None
    has_gstin: Optional[str] = None
    gstin: Optional[str] = None
    has_udyam: Optional[str] = None
    udyam_number: Optional[str] = None
    current_internet: Optional[str] = None
    current_provider: Optional[str] = None
    monthly_telecom_spend_inr: Optional[float] = None
    products_of_interest: Optional[str] = None
    contact_name: Optional[str] = None
    contact_role: Optional[str] = None
    stage_reached: Optional[str] = None
    outcome: Optional[str] = None
    drop_reason: Optional[str] = None
    contacted_date: Optional[str] = None
    needs_assessed_date: Optional[str] = None
    quote_accepted_date: Optional[str] = None
    kyc_complete_date: Optional[str] = None
    activated_date: Optional[str] = None
    days_lead_to_activation: Optional[float] = None
    customer_follow_up_calls: Optional[int] = None
    bundle_products: Optional[str] = None
    monthly_bundle_value_inr: Optional[float] = None
    one_time_setup_inr: Optional[float] = None
    contract_months: Optional[int] = None
    churned_within_6_months: Optional[str] = None
    nps_score: Optional[float] = None
    acquisition_cost_inr: Optional[float] = None


class Journey(SQLModel, table=True):
    __tablename__ = "journey"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    phone: Optional[str] = None
    identifier_type: Optional[str] = None  # gstin, udyam, none
    identifier_masked: Optional[str] = None
    identifier_raw: Optional[str] = None
    language: str = "en"
    segment: Optional[str] = None
    business_name: Optional[str] = None
    trade_name: Optional[str] = None
    legal_name: Optional[str] = None
    constitution: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    city_tier: str = "tier_1"
    employees: int = 1
    sites: int = 1
    current_spend: Optional[float] = None
    stage: str = "IDENTIFY"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    source: str = "self"  # self or partner:<id>
    handoff: bool = False
    handoff_reason: Optional[str] = None


class Quote(SQLModel, table=True):
    __tablename__ = "quote"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    journey_id: str = Field(index=True)
    bundle_json: str
    term_months: int = 12
    monthly_total: int = 0
    setup_total: int = 0
    gst_amount: int = 0
    first_invoice_total: int = 0
    tco_term: int = 0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    accepted_at: Optional[str] = None


class Consent(SQLModel, table=True):
    __tablename__ = "consent"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    journey_id: str = Field(index=True)
    purposes_json: str
    notice_version: str = "1.0"
    language: str = "en"
    granted_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    withdrawn_at: Optional[str] = None
    prev_hash: str
    hash: str


class KycCheck(SQLModel, table=True):
    __tablename__ = "kyc_check"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    journey_id: str = Field(index=True)
    doc_type: str  # gst_cert, udyam_cert, signatory_id, address_proof
    extracted_json: str
    checks_json: str
    verdict: str  # pass, review, fail
    image_sha256: str
    deleted_at: Optional[str] = None


class Order(SQLModel, table=True):
    __tablename__ = "order"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    journey_id: str = Field(index=True)
    status: str = "quote_accepted"
    promised_date: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class OrderEvent(SQLModel, table=True):
    __tablename__ = "order_event"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    order_id: str = Field(index=True)
    status: str
    message_key: str
    ts: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    simulated: bool = False


class Notification(SQLModel, table=True):
    __tablename__ = "notification"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    order_id: str = Field(index=True)
    channel: str = "whatsapp_sim"
    body: str
    language: str = "en"
    ts: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Partner(SQLModel, table=True):
    __tablename__ = "partner"
    
    id: str = Field(primary_key=True)
    name: str
    type: str  # field or channel
    region: str


class LeadScore(SQLModel, table=True):
    __tablename__ = "lead_score"
    
    journey_or_lead_id: str = Field(primary_key=True)
    score: int
    top_factors_json: str
    recommended_action: str


class AppEvent(SQLModel, table=True):
    __tablename__ = "app_event"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    event_name: str
    journey_id: Optional[str] = None
    payload_json: Optional[str] = None
    ts: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
