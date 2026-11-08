import pytest
from sqlmodel import Session
from backend.app.db import engine, init_db
from backend.app.services.kyc import run_11_kyc_checks
from backend.app.services.kyc_fixtures_data import FIXTURES_DATA

@pytest.fixture(scope="module")
def db_session():
    init_db()
    with Session(engine) as session:
        yield session

def test_k01_cancelled_gstin_fails(db_session):
    verdict, checks = run_11_kyc_checks(FIXTURES_DATA["K01"], db_session)
    assert verdict == "fail"
    chk2 = next(c for c in checks if c["id"] == "chk_2")
    assert chk2["status"] == "fail"
    assert "Cancelled" in chk2["detail"]

def test_k11_expired_bill_fails(db_session):
    verdict, checks = run_11_kyc_checks(FIXTURES_DATA["K11"], db_session)
    assert verdict == "fail"
    chk7 = next(c for c in checks if c["id"] == "chk_7")
    assert chk7["status"] == "fail"
    assert "exceeds 90-day" in chk7["detail"]

def test_k07_name_mismatch_detected(db_session):
    verdict, checks = run_11_kyc_checks(FIXTURES_DATA["K07"], db_session)
    assert verdict == "review"
    chk3 = next(c for c in checks if c["id"] == "chk_3")
    assert chk3["status"] == "review"
    assert "mismatch" in chk3["detail"].lower()

def test_all_12_fixtures_produce_valid_verdict(db_session):
    for kid in [f"K{i:02d}" for i in range(1, 13)]:
        verdict, checks = run_11_kyc_checks(FIXTURES_DATA[kid], db_session)
        assert verdict in ["pass", "review", "fail"]
        assert len(checks) == 11
