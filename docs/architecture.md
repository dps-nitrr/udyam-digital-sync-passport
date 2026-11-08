# Solution Architecture: Sync Passport

**System:** Sync Passport — GSTIN-First Digital SMB Onboarding  
**Competition:** Accel YTL Hackathon 2026 (Enterprise Track A: Project Udyam Digital)  
**Team:** `divya_tushar` (Divya Pratap Singh & Tushar Chaturvedi) — National Institute of Technology (NIT) Raipur  

---

## 1. End-to-End System Architecture

```mermaid
flowchart TD
    subgraph ClientLayer["Frontend Client Layer (Mobile PWA)"]
        UI["React 18 + Vite + TypeScript PWA<br/>Tailwind CSS (Red & Graphite Tokens)"]
        Voice["Web Speech API<br/>(Hindi & English ASR)"]
        Store["Zustand Session Store<br/>(Local Cache & Flow State)"]
        UI --- Voice
        UI --- Store
    end

    subgraph APILayer["FastAPI Gateway (Uvicorn REST API)"]
        RouterReg["/api/registry/*<br/>GSTIN & Udyam Lookup"]
        RouterAdv["/api/advisor/*<br/>Slot Extraction & Inference"]
        RouterQuote["/api/quote/*<br/>Deterministic Bundling Engine"]
        RouterKYC["/api/kyc/*<br/>11 Regulatory Rules Engine"]
        RouterTrack["/api/tracker/*<br/>Fulfillment & WhatsApp Simulator"]
        RouterLeads["/api/leads/*<br/>Back-Office Lead Triage"]
    end

    subgraph DeterministicEngine["Core Deterministic Rules Engine (No LLM)"]
        Mod36["Mod-36 GSTIN Checksum<br/>+ RapidFuzz Levenshtein Corrector"]
        SegInfer["Segment Precedence Engine<br/>(Sites >= 2, Staff >= 10, Keywords)"]
        PricingEngine["Deterministic Catalogue Rules<br/>(Eligibility, 15% 24M Discount, 18% GST)"]
        KYCRules["11 Regulatory Verification Checks<br/>(GST Status, 90-Day Utility, Name Fuzzy)"]
    end

    subgraph AIPipeline["Constrained AI & Vision Fallback"]
        LLM["Gemini Flash LLMProvider<br/>(Structured Slot Parsing Only)"]
        RegexFallback["Regex Deterministic Slot-Filler<br/>(100% Offline Demoday Failover)"]
        OCR["Pytesseract OCR + Monospace 0/O Disambiguation"]
    end

    subgraph SecurityDataLayer["DPDP Act 2023 Data & Storage Layer"]
        SQLite[("SQLModel SQLite (app.db)<br/>Journeys, Consent, Leads, Audit Logs")]
        Ledger["Append-Only Consent Ledger<br/>SHA-256 Chained Hash Verification"]
        PurgeWorker["Background Purge TTL Worker<br/>Ephemeral In-Memory RAM + 30m Auto-Scrub"]
    end

    subgraph MLPropensity["Predictive ML Model"]
        GBoost["Scikit-learn Gradient Boosting<br/>(ROC-AUC: 0.6527, Top-Decile Lift: 1.90x)"]
    end

    UI -->|JSON / REST| APILayer
    RouterReg --> Mod36
    RouterAdv --> LLM
    LLM -.->|Fallback| RegexFallback
    RouterAdv --> SegInfer
    RouterQuote --> PricingEngine
    RouterKYC --> OCR
    RouterKYC --> KYCRules
    RouterKYC --> Ledger
    RouterKYC --> PurgeWorker
    RouterLeads --> GBoost
    APILayer --> SQLite
```

---

## 2. Sequential Data Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Owner as SMB Owner / Channel Partner
    participant PWA as Mobile PWA (React)
    participant API as FastAPI Backend
    participant Reg as Mock Registry (GSTIN/Udyam)
    participant Rules as Deterministic Engine
    participant LLM as Gemini Flash / Regex
    participant KYC as 11-Rule KYC Engine
    participant Ledger as DPDP Hash Ledger

    Owner->>PWA: Speaks or enters GSTIN / Udyam ID
    PWA->>API: POST /api/registry/lookup
    API->>Rules: Mod-36 Checksum Validation
    API->>Reg: Exact match (or RapidFuzz typo match)
    Reg-->>API: Legal Name, Trade Name, Constitution, State
    API-->>PWA: Verified Business Profile (<800ms)

    Owner->>PWA: Answers 3 conversational questions (Voice/Text)
    PWA->>API: POST /api/advisor/respond
    API->>LLM: Extract structured slots {sites, employees, spend}
    API->>Rules: Algorithmic segment precedence check
    Rules-->>PWA: Inferred Segment (90%+ confidence)

    Owner->>PWA: Views Bundle Quote & Toggles Term / Add-ons
    PWA->>API: POST /api/quote/update (Payload: selections)
    API->>Rules: Check 5 catalogue invariants & calculate pricing
    Rules-->>PWA: Itemized Monthly Quote (+18% GST)

    Owner->>PWA: Grants Granular DPDP Consent
    PWA->>API: POST /api/consent/record
    API->>Ledger: Append SHA-256 hash-chained block
    Ledger-->>PWA: Cryptographic Receipt

    Owner->>PWA: Uploads KYC Specimen Documents
    PWA->>API: POST /api/kyc/verify
    API->>KYC: Run 11 deterministic checks against registry
    API->>API: Purge raw specimen images from disk
    KYC-->>PWA: Verdict: ALL_PASSED (or NEEDS_ATTENTION)

    Owner->>PWA: Tracks Order & Simulates OTP Activation
    PWA->>API: POST /api/tracker/advance-time & verify-otp
    API-->>PWA: Status: ACTIVE + Confetti Trigger
```

---

## 3. Key Architectural Decisions

1. **The Golden Rule (Zero LLM Pricing or KYC):** The LLM is used strictly as a parser to convert conversational voice/text into structured integers. Product eligibility, bundling dependencies, and pricing are 100% deterministic Python code.
2. **Zero-Infra Portability:** Runs entirely in a single process via SQLite and local models. Zero cloud dependency ensures 100% demo reliability.
3. **DPDP Act 2023 Compliance:** Purpose-specific consent, ephemeral RAM OCR extraction, immediate file purge, and an immutable cryptographic SHA-256 chained audit trail.
