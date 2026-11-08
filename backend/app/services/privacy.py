import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from backend.app.config import settings

def mask_identifier(ident: Optional[str]) -> str:
    """Masks identifier showing first 2 and last 4 characters."""
    if not ident:
        return ""
    clean = ident.strip()
    if len(clean) <= 6:
        return "X" * len(clean)
    first2 = clean[:2]
    last4 = clean[-4:]
    masked_middle = "X" * (len(clean) - 6)
    return f"{first2}{masked_middle}{last4}"

def compute_hash_chain(prev_hash: str, payload: Dict[str, Any]) -> str:
    """Computes tamper-evident SHA-256 hash for consent ledger."""
    canonical_payload = json.dumps(payload, sort_keys=True)
    raw_str = f"{prev_hash}:{canonical_payload}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

def purge_expired_uploads():
    """Deletes uploaded temporary files older than UPLOAD_TTL_MINUTES."""
    upload_dir = settings.UPLOAD_DIR
    if not upload_dir.exists():
        return
    now = time.time()
    ttl_seconds = settings.UPLOAD_TTL_MINUTES * 60
    for item in upload_dir.iterdir():
        if item.is_file():
            file_age = now - item.stat().st_mtime
            if file_age > ttl_seconds:
                try:
                    item.unlink()
                except Exception as e:
                    print(f"Error purging {item}: {e}")
