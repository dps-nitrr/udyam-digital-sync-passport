# "Sync Passport" — Competition Demo Walkthrough Script

**App URL for Judges:** `http://localhost:5173/?demo=1`  
**API Documentation:** `http://localhost:8000/docs`  
**Brand Identity:** Accel Business (Red & Graphite Palette, DPDP Compliant)

---

## 1. Executive Summary & Problem Framing (1 Minute Pitch)

- **The Problem:** Indian SMB digital onboarding suffers a **58% digital drop rate** caused by 3 friction points:
  1. Manual multi-page entry forms and redundant document requests.
  2. Confusing a la carte telecom pricing with hidden installation and router fees.
  3. Slow, paper-heavy KYC verification taking up to 18 days with 50% rejection rates.
- **The Solution ("Sync Passport"):** A mobile-first, GSTIN-first onboarding engine that:
  - Turns **1 government identifier** (GSTIN or Udyam number) into verified company records in < 1 second.
  - Predicts the business segment and generates **ONE transparent monthly price** with 100% deterministic rules.
  - Automates 11 KYC checks with zero-retention privacy (specimens purged immediately, retaining only an immutable SHA-256 hash receipt).
  - Equips back-office advisors with an **ML propensity model** (Top-decile lift: **1.90x**) to triage dropped leads.

---

## 2. Live Demo Personas Cheat Sheet

The judge bar appears at the top when running with `?demo=1`. Clicking any persona pre-fills the identifier field and executes the live government registry lookup and rules engine.

| Persona ID | Business Entity | Identifier | Language | Demo Highlights |
|---|---|---|---|---|
| **D1** | Suresh Provision & General Store | `19EOGXH4115Y1ZL` | English | **Active Retailer**: Instant lookup, infers Micro Retail, recommends AirFiber starter + POS billing + WhatsApp API. |
| **D2** | Maa Tara Sweets | `UDYAM-WB-00-5053330` | Hindi (हिंदी) | **No-GST Path**: Validates Udyam registry in Hindi, recommends GST-free AirFiber starter (P04). |
| **D3** | Balaji Dental Care LLP | `32TTNXB7384T1ZW` | English | **Professional Office**: Infers Healthcare clinic, recommends Symmetric 100 Mbps Fibre + Cloud Backup + Workspace email. |
| **D4** | Blue Lotus Kitchens Pvt Ltd | `19JENXB8672I1ZA` | English | **Multi-Site Chain (5 Stores)**: Recommends 24m term, branch failover + managed Wi-Fi per store. |
| **D5** | Ganesh Woodcraft | `27XUIXG0767D1ZP` | English | **Small Manufacturer (20 staff)**: Leased line + hardware firewall + 24m term pricing. |
| **D6** | Krishna Enterprises | `37IHKXV5167L1ZS` | English | **Cancelled GSTIN Alert**: Flags compliance issue, restricts sale of GSTIN-dependent products, routes to GST-free starter without crashing. |

---

## 3. Step-by-Step Scripted Walkthrough

### Step 1: Identifier Entry & Voice Search (`Entry.tsx`)
1. Open `http://localhost:5173/?demo=1`.
2. Notice the "Judge Demo Pre-fills" bar at the top.
3. Test speech recognition by clicking the **Microphone Icon** (uses Web Speech API for `hi-IN` and `en-IN`).
4. Click **D1** (or type `19EOGXH4115Y1ZL`) and press **Fetch Business Details**.
5. *Talking point:* "We don't ask the owner to type 20 fields. We leverage government registries to fetch legal entity name, trade name, constitution, and state in under 800 milliseconds."

### Step 2: Confirmation & Segment Inference (`BusinessConfirm.tsx`)
1. Review the verified business card: "Suresh Provision & General Store", Proprietorship, Active GST.
2. Highlight the **Identified Business Segment** pill: *Micro retail & services (85% Match)*.
3. Click **Confirm & Customize Plan**.

### Step 3: 3-Question Solution Advisor (`Advisor.tsx`)
1. Explain the state machine: asks at most 3 lightweight confirming questions (Locations, Staff size, Current spend).
2. Answer:
   - Sites: `1 Location`
   - Employees: `1 - 4 Members`
   - Current bill: `₹2,000 - ₹5,000 / mo`
3. *Talking point:* "The LLM never sets a price or chooses a product. All bundling logic is pure deterministic code. If the customer operates 10+ sites, the system automatically triggers an Enterprise Solution Architect handoff."

### Step 4: Transparent Quote & Add-On Toggles (`Quote.tsx`)
1. Point to the **Hero Monthly Price**: `₹X / month + 18% GST`.
2. Highlight the **Savings Banner**: Shows exact monthly savings compared to current telecom bills.
3. Toggle contract term from **12 Months** to **24 Months**:
   - *Key architectural point:* "The frontend never calculates prices. The toggle calls `/api/quote/update`, and the backend pricing engine updates unit rates, 18% GST, and first invoice totals live."
4. Click `+` / `-` on quantity steppers or toggle an Add-On:
   - Notice dependency handling: If a product requires a primary broadband line, the engine automatically adds it or displays a toast.
5. Expand the collapsible **Products Excluded For Your Profile** drawer:
   - Shows regulatory reasons why high-end products (e.g. SIP Trunk, Leased Line) are excluded for a micro retailer.
6. Click **Accept Quote & Proceed to Verification**.

### Step 5: DPDP 2023 Consent Ledger (`Consent.tsx`)
1. Review the purpose-specific consent checkboxes (Entity verification, address feasibility, authorized signatory).
2. Point out the zero-retention notice and the live **Cryptographic Hash Receipt**:
   - `sha256(prev_hash + purposes + timestamp)` creates a verifiable, tamper-evident hash chain.
3. Click **Agree & Upload KYC Documents**.

### Step 6: KYC Verification & Specimen Fixtures (`Kyc.tsx`)
1. The 4 upload cards appear for GST cert, Signatory ID, Address Proof, and Board Resolution.
2. In the Judge Specimen Bar, click **K01**:
   - Shows **FAIL** / **NEEDS ATTENTION** in dark burgundy (distinct from brand red) because GSTIN is cancelled.
3. Click **K02**:
   - Shows **PASSED** because monospace `0` vs `O` OCR confusion was automatically resolved against the registry.
4. Click **K07**:
   - Shows **NEEDS ATTENTION** because signatory name on ID does not match registry records.
5. Click **K11**:
   - Shows **NEEDS ATTENTION** because electricity bill is dated 2025-10-31 (>90 days old relative to demo date 2026-07-15).
6. Click **K03** (Clean Pass) and click **Proceed to Order Activation**.

### Step 7: Live Order Tracker & WhatsApp Simulator (`Tracker.tsx`)
1. View the **6-stage fulfillment milestone chain** with the promised installation date.
2. Point out the **AirFiber Delay Compensation SLA** (₹100 credit per day past SLA).
3. View the **Live WhatsApp Customer Feed** inside the simulated phone bezel.
4. Click **Demo: Advance 24 Hours (+1 Day)**:
   - Simulates field feasibility and equipment installation milestones.
5. Click **Simulate OTP**:
   - Enter demo code `123456` and click Verify.
   - Service becomes Active and celebratory confetti triggers!

---

## 4. Back-Office Console Walkthrough (Advisor / Partner Triage)

1. Click the **Back-Office** button in the top navigation.
2. **Unclosed Leads Triage (`Leads.tsx`):**
   - View 5,000 historical synthetic leads ranked by the Scikit-learn **Propensity Model**.
   - Filter by **High Propensity** (Top Decile with **1.90x lift**).
   - Assign field leads to local partners (`Rajesh Verma`, `Priya Deshmukh`).
3. **Funnel Analytics (`Dashboard.tsx`):**
   - Review the funnel drop-off bar chart from Contacted to Activated.
   - Explain the **58.4% Digital-Fixable Drops**: Over half of past dropped leads were lost due to KYC delays and opaque pricing, directly resolved by Sync Passport.
