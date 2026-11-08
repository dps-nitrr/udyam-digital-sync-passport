import re
from typing import Optional, Dict, Any, Tuple
from sqlmodel import Session, select
from rapidfuzz.distance import Levenshtein
from backend.app.models import RegistryGSTIN

CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHAR_INDEX = {c: i for i, c in enumerate(CHARSET)}
# Format: 2 digits + 5 uppercase letters (4th can be X) + 4 digits + 1 letter + 1 char (1-9A-Z) + Z + 1 char
GSTIN_REGEX = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")

def normalize_gstin(gstin: str) -> str:
    return gstin.strip().upper().replace(" ", "")

def check_gstin_format(gstin: str) -> bool:
    return bool(GSTIN_REGEX.match(gstin))

def calculate_checksum_char(gstin_14: str) -> str:
    s = 0
    for i in range(14):
        ch = gstin_14[i]
        idx = CHAR_INDEX.get(ch, 0)
        multiplier = 1 if (i % 2 == 0) else 2
        v = idx * multiplier
        s += (v // 36) + (v % 36)
    expected_idx = (36 - (s % 36)) % 36
    return CHARSET[expected_idx]

def check_gstin_checksum(gstin: str) -> bool:
    if len(gstin) != 15 or not check_gstin_format(gstin):
        return False
    return calculate_checksum_char(gstin[:14]) == gstin[14]

def find_gstin_suggestion(raw_gstin: str, session: Session) -> Optional[str]:
    """Find a registry GSTIN with edit distance 1 (same length) for typo suggestion."""
    if len(raw_gstin) != 15:
        return None
    # Look through registry for candidates
    # To be fast, candidate must share at least state prefix (first 2 chars) or similar
    state_prefix = raw_gstin[:2]
    stmt = select(RegistryGSTIN)
    # Check candidates starting with state prefix or entire table if needed
    candidates = session.exec(stmt.where(RegistryGSTIN.gstin.startswith(state_prefix))).all()
    if not candidates:
        candidates = session.exec(stmt).all()
        
    for c in candidates:
        if Levenshtein.distance(raw_gstin, c.gstin) == 1:
            return c.gstin
    return None

def lookup_gstin(gstin_input: str, session: Session) -> Dict[str, Any]:
    norm = normalize_gstin(gstin_input)
    fmt_ok = check_gstin_format(norm)
    chk_ok = check_gstin_checksum(norm) if fmt_ok else False
    
    reg_entry = session.get(RegistryGSTIN, norm)
    
    suggestion = None
    if (not reg_entry or not chk_ok):
        suggestion = find_gstin_suggestion(norm, session)
        
    if not reg_entry:
        return {
            "valid_format": fmt_ok,
            "checksum_ok": chk_ok,
            "found": False,
            "status": None,
            "legal_name": None,
            "trade_name": None,
            "constitution": None,
            "address": None,
            "state": None,
            "suggestion": suggestion,
            "gst_status_issue": False
        }
        
    status = reg_entry.status
    gst_status_issue = (status in ["Cancelled", "Suspended"])
    
    return {
        "valid_format": fmt_ok,
        "checksum_ok": chk_ok,
        "found": True,
        "status": status,
        "legal_name": reg_entry.legal_name,
        "trade_name": reg_entry.trade_name,
        "constitution": reg_entry.constitution,
        "address": reg_entry.principal_place_of_business,
        "state": reg_entry.state,
        "suggestion": suggestion,
        "gst_status_issue": gst_status_issue
    }
