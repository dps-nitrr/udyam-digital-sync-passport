import re
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from backend.app.models import RegistryUdyam

# Format: UDYAM-XX-00-0000000 (e.g. UDYAM-KL-00-3078801)
UDYAM_REGEX = re.compile(r"^UDYAM-[A-Z]{2}-\d{2}-\d{7}$")

def normalize_udyam(udyam_str: str) -> str:
    return udyam_str.strip().upper().replace(" ", "")

def check_udyam_format(udyam_str: str) -> bool:
    return bool(UDYAM_REGEX.match(udyam_str))

def lookup_udyam(udyam_input: str, session: Session) -> Dict[str, Any]:
    norm = normalize_udyam(udyam_input)
    fmt_ok = check_udyam_format(norm)
    
    reg_entry = session.get(RegistryUdyam, norm)
    if not reg_entry:
        return {
            "valid_format": fmt_ok,
            "found": False,
            "udyam_number": norm,
            "enterprise_name": None,
            "enterprise_type": None,
            "major_activity": None,
            "nic_description": None,
            "city": None,
            "state": None,
            "date_of_registration": None
        }
        
    return {
        "valid_format": fmt_ok,
        "found": True,
        "udyam_number": reg_entry.udyam_number,
        "enterprise_name": reg_entry.enterprise_name,
        "enterprise_type": reg_entry.enterprise_type,
        "major_activity": reg_entry.major_activity,
        "nic_description": reg_entry.nic_description,
        "city": reg_entry.city,
        "state": reg_entry.state,
        "date_of_registration": reg_entry.date_of_registration
    }
