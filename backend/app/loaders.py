import json
import pandas as pd
import numpy as np
from pathlib import Path
from sqlmodel import Session, select
from backend.app.config import settings
from backend.app.db import engine
from backend.app.models import Product, RegistryGSTIN, RegistryUdyam, Lead, Partner

def load_products(session: Session, data_dir: Path):
    file_path = data_dir / "product_catalogue.csv"
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    existing = session.exec(select(Product)).first()
    if existing:
        return

    df = pd.read_csv(file_path).replace({np.nan: None})
    for _, row in df.iterrows():
        # tiers split on ;
        tiers_raw = str(row["available_city_tiers"]) if row["available_city_tiers"] else ""
        tiers = [t.strip() for t in tiers_raw.split(";") if t.strip()]

        # requires_one_of split on |
        req_one_raw = str(row["requires_one_of"]) if row["requires_one_of"] else ""
        requires_one_of = [r.strip() for r in req_one_raw.split("|") if r.strip()]

        # target_segments split on ;
        targets_raw = str(row["target_segments"]) if row["target_segments"] else ""
        target_segments = [s.strip() for s in targets_raw.split(";") if s.strip()]

        product = Product(
            product_id=str(row["product_id"]).strip(),
            category=str(row["category"]).strip(),
            product_name=str(row["product_name"]).strip(),
            description=str(row["description"]).strip(),
            unit=str(row["unit"]).strip(),
            price_min=int(row["price_min_inr_per_month"]),
            price_max=int(row["price_max_inr_per_month"]),
            setup_fee=int(row["one_time_setup_inr"]),
            min_contract_months=int(row["min_contract_months"]),
            tiers_json=json.dumps(tiers),
            min_employees=int(row["min_employees"]),
            min_sites=int(row["min_sites"]),
            requires_gstin=True if str(row["requires_gstin"]).strip().upper() == "Y" else False,
            requires_one_of_json=json.dumps(requires_one_of),
            install_days=int(row["typical_install_days"]),
            target_segments_json=json.dumps(target_segments),
        )
        session.add(product)
    session.commit()
    print("Loaded products catalogue.")


def load_gstin_registry(session: Session, data_dir: Path):
    file_path = data_dir / "mock_gstin_registry.csv"
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    existing = session.exec(select(RegistryGSTIN)).first()
    if existing:
        return

    df = pd.read_csv(file_path).replace({np.nan: ""})
    gstin_objs = []
    for _, row in df.iterrows():
        gstin_objs.append(
            RegistryGSTIN(
                gstin=str(row["gstin"]).strip().upper(),
                legal_name=str(row["legal_name"]).strip(),
                trade_name=str(row["trade_name"]).strip(),
                constitution=str(row["constitution"]).strip(),
                principal_place_of_business=str(row["principal_place_of_business"]).strip(),
                state=str(row["state"]).strip(),
                registration_date=str(row["registration_date"]).strip(),
                status=str(row["status"]).strip(),
            )
        )
    session.add_all(gstin_objs)
    session.commit()
    print(f"Loaded {len(gstin_objs)} GSTIN registry rows.")


def load_udyam_registry(session: Session, data_dir: Path):
    file_path = data_dir / "mock_udyam_registry.csv"
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    existing = session.exec(select(RegistryUdyam)).first()
    if existing:
        return

    df = pd.read_csv(file_path).replace({np.nan: ""})
    udyam_objs = []
    for _, row in df.iterrows():
        udyam_objs.append(
            RegistryUdyam(
                udyam_number=str(row["udyam_number"]).strip().upper(),
                enterprise_name=str(row["enterprise_name"]).strip(),
                enterprise_type=str(row["enterprise_type"]).strip(),
                major_activity=str(row["major_activity"]).strip(),
                nic_description=str(row["nic_description"]).strip(),
                state=str(row["state"]).strip(),
                city=str(row["city"]).strip(),
                date_of_registration=str(row["date_of_registration"]).strip(),
            )
        )
    session.add_all(udyam_objs)
    session.commit()
    print(f"Loaded {len(udyam_objs)} Udyam registry rows.")


def load_leads(session: Session, data_dir: Path):
    file_path = data_dir / "smb_leads.csv"
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    existing = session.exec(select(Lead)).first()
    if existing:
        return

    df = pd.read_csv(file_path).replace({np.nan: None})
    lead_objs = []
    for _, row in df.iterrows():
        lead_objs.append(
            Lead(
                lead_id=str(row["lead_id"]).strip(),
                created_date=str(row["created_date"]) if row["created_date"] is not None else None,
                lead_source=str(row["lead_source"]) if row["lead_source"] is not None else None,
                business_name=str(row["business_name"]) if row["business_name"] is not None else None,
                business_type=str(row["business_type"]) if row["business_type"] is not None else None,
                segment=str(row["segment"]) if row["segment"] is not None else None,
                city=str(row["city"]) if row["city"] is not None else None,
                city_tier=str(row["city_tier"]) if row["city_tier"] is not None else None,
                state=str(row["state"]) if row["state"] is not None else None,
                preferred_language=str(row["preferred_language"]) if row["preferred_language"] is not None else None,
                employee_count=int(row["employee_count"]) if row["employee_count"] is not None else None,
                num_sites=int(row["num_sites"]) if row["num_sites"] is not None else None,
                annual_turnover_band=str(row["annual_turnover_band"]) if row["annual_turnover_band"] is not None else None,
                has_gstin=str(row["has_gstin"]) if row["has_gstin"] is not None else None,
                gstin=str(row["gstin"]) if row["gstin"] is not None else None,
                has_udyam=str(row["has_udyam"]) if row["has_udyam"] is not None else None,
                udyam_number=str(row["udyam_number"]) if row["udyam_number"] is not None else None,
                current_internet=str(row["current_internet"]) if row["current_internet"] is not None else None,
                current_provider=str(row["current_provider"]) if row["current_provider"] is not None else None,
                monthly_telecom_spend_inr=float(row["monthly_telecom_spend_inr"]) if row["monthly_telecom_spend_inr"] is not None else None,
                products_of_interest=str(row["products_of_interest"]) if row["products_of_interest"] is not None else None,
                contact_name=str(row["contact_name"]) if row["contact_name"] is not None else None,
                contact_role=str(row["contact_role"]) if row["contact_role"] is not None else None,
                stage_reached=str(row["stage_reached"]) if row["stage_reached"] is not None else None,
                outcome=str(row["outcome"]) if row["outcome"] is not None else None,
                drop_reason=str(row["drop_reason"]) if row["drop_reason"] is not None else None,
                contacted_date=str(row["contacted_date"]) if row["contacted_date"] is not None else None,
                needs_assessed_date=str(row["needs_assessed_date"]) if row["needs_assessed_date"] is not None else None,
                quote_accepted_date=str(row["quote_accepted_date"]) if row["quote_accepted_date"] is not None else None,
                kyc_complete_date=str(row["kyc_complete_date"]) if row["kyc_complete_date"] is not None else None,
                activated_date=str(row["activated_date"]) if row["activated_date"] is not None else None,
                days_lead_to_activation=float(row["days_lead_to_activation"]) if row["days_lead_to_activation"] is not None else None,
                customer_follow_up_calls=int(row["customer_follow_up_calls"]) if row["customer_follow_up_calls"] is not None else None,
                bundle_products=str(row["bundle_products"]) if row["bundle_products"] is not None else None,
                monthly_bundle_value_inr=float(row["monthly_bundle_value_inr"]) if row["monthly_bundle_value_inr"] is not None else None,
                one_time_setup_inr=float(row["one_time_setup_inr"]) if row["one_time_setup_inr"] is not None else None,
                contract_months=int(row["contract_months"]) if row["contract_months"] is not None else None,
                churned_within_6_months=str(row["churned_within_6_months"]) if row["churned_within_6_months"] is not None else None,
                nps_score=float(row["nps_score"]) if row["nps_score"] is not None else None,
                acquisition_cost_inr=float(row["acquisition_cost_inr"]) if row["acquisition_cost_inr"] is not None else None,
            )
        )
    session.add_all(lead_objs)
    session.commit()
    print(f"Loaded {len(lead_objs)} leads.")


def seed_partners(session: Session):
    existing = session.exec(select(Partner)).first()
    if existing:
        return
    partners = [
        Partner(id="P-DEL-01", name="Rajesh Verma (Field)", type="field", region="Delhi NCR"),
        Partner(id="P-MUM-01", name="Priya Deshmukh (Channel)", type="channel", region="Mumbai"),
        Partner(id="P-BLR-01", name="Karthik Rao (Field)", type="field", region="Bengaluru"),
        Partner(id="P-HYD-01", name="Suresh Reddy (Channel)", type="channel", region="Hyderabad"),
    ]
    session.add_all(partners)
    session.commit()
    print("Seeded partners.")


def load_all_csvs():
    with Session(engine) as session:
        load_products(session, settings.DATA_DIR)
        load_gstin_registry(session, settings.DATA_DIR)
        load_udyam_registry(session, settings.DATA_DIR)
        load_leads(session, settings.DATA_DIR)
        seed_partners(session)

if __name__ == "__main__":
    from backend.app.db import init_db
    init_db()
