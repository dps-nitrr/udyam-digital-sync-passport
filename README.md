# Sync Passport — GSTIN-First SMB Onboarding Prototype

> **Airtel SYNC Hackathon 2026 | Enterprise Track A: Project Udyam Digital**  
> **Team:** divya_tushar — Divya Pratap Singh & Tushar Chaturvedi, National Institute of Technology (NIT) Raipur  
> **Repository:** [https://github.com/dps-nitrr/udyam-digital-sync-passport](https://github.com/dps-nitrr/udyam-digital-sync-passport)  
> **Compliance:** 100% DPDP Act 2023 compliant with cryptographic SHA-256 hash-chain consent ledger and zero image retention.

---

## 🏆 Official Competition Deliverables (Submission Index)

| # | Deliverable | Location / Access Link |
|---|---|---|
| **1** | **3-Minute Video Walkthrough** | 🎥 **[Watch Live Demo on YouTube](https://youtu.be/GSbkx6_qmAQ)** |
| **2** | **Source Code Repository** | 💻 **[GitHub Repository (main branch)](https://github.com/dps-nitrr/udyam-digital-sync-passport)** |
| **3** | **Solution Architecture Diagram** | 🏛️ **[docs/architecture.md](./docs/architecture.md)** *(Mermaid diagrams, data flows, and design rationale)* |
| **4** | **Business Case Deck (7 Slides)** | 📊 **[divya_tushar_Sync_Submission_ALIGNED.pptx](./divya_tushar_Sync_Submission_ALIGNED.pptx)** *(Strict 16:9 canvas, KPI scorecards, zero text overflow)* |
| **5** | **DPDP Act 2023 Privacy Note** | 🛡️ **[docs/privacy_note.md](./docs/privacy_note.md)** *(Section 6 notices, purpose limitation, and 30-min purge TTL)* |

---

## 🚀 Quick Start (Running the Prototype)

### 1. Backend (Python 3.11+ / FastAPI)

```bash
# In project root
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r backend/requirements.txt  # or: pip install fastapi sqlmodel pandas rapidfuzz scikit-learn uvicorn httpx python-multipart pillow

# Run the FastAPI server (auto-loads CSV registries on first start)
python -m uvicorn backend.app.main:app --reload --port 8000
```

- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- SQLite Database: `app.db` (auto-seeded with 25 catalogue products, 5,000 synthetic leads, 3,534 GSTINs, and 2,723 Udyam rows)

---

### 2. Frontend (React 18 + Vite + TypeScript + Tailwind CSS)

```bash
cd frontend
npm install
npm run dev
```

- **Judge Demo Mode:** [http://localhost:5173/?demo=1](http://localhost:5173/?demo=1) (activates the top pre-fill bar)
- **Production Build:** `npm run build`

---

## 🧪 Running the Test Suite

All 22 deterministic tests specified in Section 16 of `SPEC.md` are passing:

```bash
# Run all backend tests
python -m pytest backend/tests/ -v

# Run KYC K01-K12 Specimen Fixture Evaluation
python backend/scripts/run_kyc_fixtures.py

# Re-train Propensity Model (writes models/propensity.joblib & models/metrics.json)
python backend/scripts/train_propensity.py
```

### Test Coverage Highlights:
- `test_gstin.py`: All 3,534 registry GSTINs pass format + Mod-36 checksum; 20 mutated test GSTINs fail.
- `test_eligibility.py`: Pure rules engine checks city tier, employee count, site count, GSTIN requirement, and dependencies.
- `test_bundles_and_pricing.py`: 200 random leads evaluated with zero eligibility violations; transparent 18% GST math verified.
- `test_kyc.py`: Verified against K01 (Cancelled GSTIN), K02 (Monospace OCR correction), K07 (Signatory name mismatch), K11 (Expired utility bill > 90 days), and all 12 specimens.
- `test_privacy_and_consent.py`: DPDP consent ledger hash tampering detection and 30-minute upload purge verified.
- `test_journeys_d1_d6.py`: Full end-to-end persona journeys D1 through D6 verified.

---

## 📱 Live Demo Walkthrough (Personas D1–D6)

When opening `http://localhost:5173/?demo=1`, use the judge bar at the top to test live scenarios:

1. **D1: Active Retailer (`19EOGXH4115Y1ZL`)**
   - Suresh Provision & General Store (West Bengal) — Active GSTIN.
   - Infers Micro Retail segment, recommends AirFiber starter + POS counter machine + official WhatsApp Business API.
2. **D2: No-GST Path (`UDYAM-WB-00-5053330`)**
   - Maa Tara Sweets — Micro enterprise with valid Udyam registration.
   - Hindi localization flow; recommends GST-free AirFiber starter (P04).
3. **D3: Dental Clinic (`32TTNXB7384T1ZW`)**
   - Balaji Dental Care LLP (Kerala).
   - Infers Professional Office segment; recommends 100 Mbps Symmetric Fibre + Automated Cloud Backup + Custom Domain Workspace.
4. **D4: 5-Site Restaurant Chain (`19JENXB8672I1ZA`)**
   - Blue Lotus Kitchens Pvt Ltd (West Bengal).
   - Infers Multi-Site segment; recommends 24m contract, 4G cellular branch failover + managed Wi-Fi per store.
5. **D5: Small Manufacturer (`27XUIXG0767D1ZP`)**
   - Ganesh Woodcraft (Maharashtra) — 20 staff workshop.
   - Infers Small Manufacturer; recommends 1:1 Leased Line + Hardware Firewall + 24m term pricing.
6. **D6: Cancelled GSTIN (`37IHKXV5167L1ZS`)**
   - Krishna Enterprises (Andhra Pradesh) — GSTIN is Cancelled.
   - System flags compliance alert, restricts GST-dependent products, and routes safely to GST-free starter without crashing.

---

## 🏛️ Architecture & Golden Rules

```
                      +-----------------------------+
                      | React 18 Mobile PWA (390px) |
                      +--------------+--------------+
                                     | REST / JSON
                                     v
                      +-----------------------------+
                      |       FastAPI Backend       |
                      +--------------+--------------+
                                     |
    +-----------------+--------------+-----------------+-----------------+
    |                 |                                |                 |
    v                 v                                v                 v
[Registry Service] [Rules Engine: Bundles/Pricing] [KYC Engine] [Propensity Model]
(GSTIN / Udyam)    (100% Deterministic Code)       (11 Rules)   (Top Decile: 1.90x)
```

- **Golden Rule:** The LLM never decides a product, a price, or a KYC pass/fail. All business logic is deterministic code.
- **Offline Reliability:** `LLM_PROVIDER=none` in `.env` produces a 100% functional demo with zero external API dependencies.
- **Privacy Standard:** Zero raw document image storage; immutable SHA-256 consent hash ledger.

---

## 📑 Additional Documentation

- [Solution Architecture & Data Flow](docs/architecture.md)
- [Submission Presentation Deck (7 Slides)](divya_tushar_Sync_Submission_ALIGNED.pptx)
- [Detailed Demo Walkthrough Script](docs/demo_script.md)
- [DPDP Act 2023 Compliance Note](docs/privacy_note.md)
- [KYC Fixture Evaluation Results (K01-K12)](docs/kyc_results.md)
