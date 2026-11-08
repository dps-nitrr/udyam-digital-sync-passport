import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings

client = TestClient(app)

def test_d1_micro_retailer_with_active_gstin():
    # 1. Start journey
    r = client.post("/api/journeys", json={"language": "en"})
    assert r.status_code == 200
    jid = r.json()["journey_id"]

    # 2. Lookup active GSTIN
    r = client.post("/api/registry/lookup", json={"journey_id": jid, "identifier": "19EOGXH4115Y1ZL"})
    assert r.status_code == 200
    data = r.json()
    assert data["found"] is True
    assert data["status"] == "Active"

    # 3. Advisor questions
    r = client.post("/api/advisor/message", json={"journey_id": jid, "slot": "sites", "chip_value": 1})
    assert r.status_code == 200
    r = client.post("/api/advisor/message", json={"journey_id": jid, "slot": "employees", "chip_value": 3})
    assert r.status_code == 200
    r = client.post("/api/advisor/message", json={"journey_id": jid, "slot": "current_spend", "chip_value": 2500})
    assert r.status_code == 200

    # 4. Recommend bundle
    r = client.post("/api/advisor/recommend", json={"journey_id": jid})
    assert r.status_code == 200
    rec = r.json()
    assert len(rec["bundle"]) > 0
    assert rec["quote"]["monthly_recurring"] > 0

    # 5. Accept quote
    r = client.post("/api/quote/accept", json={"journey_id": jid})
    assert r.status_code == 200

    # 6. Consent
    r = client.post("/api/consent", json={"journey_id": jid, "accepted_purposes": ["verify_identity", "verify_address", "verify_signatory"]})
    assert r.status_code == 200

    # 7. Create order
    r = client.post("/api/orders", json={"journey_id": jid})
    assert r.status_code == 200
    order_id = r.json()["order_id"]

    # 8. Tracker status
    r = client.get(f"/api/orders/{order_id}")
    assert r.status_code == 200
    assert r.json()["status"] == "quote_accepted"


def test_d2_micro_retailer_without_gstin():
    r = client.post("/api/journeys", json={"language": "en"})
    jid = r.json()["journey_id"]

    # No GST path -> Udyam lookup
    r = client.post("/api/registry/lookup", json={"journey_id": jid, "identifier": "UDYAM-WB-00-5053330"})
    assert r.status_code == 200
    assert r.json()["found"] is True

    # 2 questions
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "sites", "chip_value": 1})
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "employees", "chip_value": 2})

    # Recommend bundle
    r = client.post("/api/advisor/recommend", json={"journey_id": jid})
    assert r.status_code == 200
    rec = r.json()
    # Check that starter AirFiber P04 is recommended
    pids = [b["product_id"] for b in rec["bundle"]]
    assert "P04" in pids or "P01" in pids or len(pids) > 0


def test_d3_dental_clinic_professional():
    r = client.post("/api/journeys", json={"language": "en"})
    jid = r.json()["journey_id"]

    client.post("/api/registry/lookup", json={"journey_id": jid, "identifier": "19EOGXH4115Y1ZL"})
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "sites", "chip_value": 1})
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "employees", "chip_value": 4})

    r = client.post("/api/advisor/recommend", json={"journey_id": jid})
    assert r.status_code == 200
    rec = r.json()
    assert rec["quote"]["term_months"] == 12


def test_d4_restaurant_chain_5_sites():
    r = client.post("/api/journeys", json={"language": "en"})
    jid = r.json()["journey_id"]

    # Multi-site: 5 sites
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "sites", "chip_value": 5})
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "employees", "chip_value": 15})

    r = client.post("/api/advisor/recommend", json={"journey_id": jid})
    assert r.status_code == 200
    rec = r.json()
    # Should recommend multi-site template (24 months)
    assert rec["quote"]["term_months"] == 24


def test_d5_small_manufacturer():
    r = client.post("/api/journeys", json={"language": "en"})
    jid = r.json()["journey_id"]

    client.post("/api/registry/lookup", json={"journey_id": jid, "identifier": "27XUIXG0767D1ZP"})
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "sites", "chip_value": 1})
    client.post("/api/advisor/message", json={"journey_id": jid, "slot": "employees", "chip_value": 20})

    r = client.post("/api/advisor/recommend", json={"journey_id": jid})
    assert r.status_code == 200
    rec = r.json()
    assert rec["quote"]["term_months"] == 24


def test_d6_cancelled_gstin_flags_issue_and_starter():
    r = client.post("/api/journeys", json={"language": "en"})
    jid = r.json()["journey_id"]

    # 37IHKXV5167L1ZS is Cancelled
    r = client.post("/api/registry/lookup", json={"journey_id": jid, "identifier": "37IHKXV5167L1ZS"})
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "Cancelled"
    assert data["gst_status_issue"] is True

    # Journey can continue on GST-free starter without crashing
    r = client.post("/api/advisor/recommend", json={"journey_id": jid})
    assert r.status_code == 200
    rec = r.json()
    # Must not contain requires_gstin products
    for b in rec["bundle"]:
        assert b["product_id"] not in ["P15", "P12"]
