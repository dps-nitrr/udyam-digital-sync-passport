import pytest
import os
import time
from backend.app.services.privacy import mask_identifier, compute_hash_chain, purge_expired_uploads
from backend.app.config import settings

def test_mask_identifier():
    # Style: 37XXXXXXXXXXXZS (first 2 + masked middle + last 4)
    raw_gstin = "37IHKXV5167L1ZS"
    masked = mask_identifier(raw_gstin)
    assert masked.startswith("37")
    assert masked.endswith("1ZS")
    assert len(masked) == len(raw_gstin)
    assert "X" in masked

    raw_udyam = "UDYAM-KL-00-3078801"
    masked_udyam = mask_identifier(raw_udyam)
    assert masked_udyam.startswith("UD")
    assert masked_udyam.endswith("8801")
    assert len(masked_udyam) == len(raw_udyam)

def test_consent_ledger_tampering_breaks_hash():
    prev_hash = "GENESIS_HASH_00000000000000000000000000000000"
    payload1 = {"journey_id": "J1", "purposes": ["p1", "p2"], "notice_version": "1.0"}
    hash1 = compute_hash_chain(prev_hash, payload1)

    payload2 = {"journey_id": "J2", "purposes": ["p1", "p2", "p3"], "notice_version": "1.0"}
    hash2 = compute_hash_chain(hash1, payload2)

    # 1. Normal chain verifies
    assert hash2 == compute_hash_chain(hash1, payload2)

    # 2. Tampering with payload1 changes hash1
    tampered_payload1 = {"journey_id": "J1", "purposes": ["p1"], "notice_version": "1.0"}
    tampered_hash1 = compute_hash_chain(prev_hash, tampered_payload1)
    assert tampered_hash1 != hash1

    # And breaks payload2 verification with tampered_hash1
    assert compute_hash_chain(tampered_hash1, payload2) != hash2

def test_upload_purge(tmp_path):
    settings.UPLOAD_DIR = tmp_path
    settings.UPLOAD_TTL_MINUTES = 0  # immediate purge

    test_file = tmp_path / "test_doc.png"
    test_file.write_text("dummy binary content")
    assert test_file.exists()

    # Backdate mtime
    past_time = time.time() - 100
    os.utime(test_file, (past_time, past_time))

    purge_expired_uploads()
    assert not test_file.exists()
