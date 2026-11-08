# DPDP Act 2023 Compliance Architecture Note

**System:** Sync Passport — GSTIN-First SMB Onboarding Engine  
**Entity:** Accel Business / Airtel SYNC  
**Reference Regulation:** Digital Personal Data Protection Act, 2023 (DPDP Act)

---

## 1. Principles of Architecture

Sync Passport was architected under the principle of **Data Minimisation & Purpose Limitation** set forth in Section 4 and Section 6 of the DPDP Act 2023. At no point does the system store unnecessary personal identifiers, unredacted biometric cards, or specimen image files on disk.

```
+-----------------------------------------------------------------------------------+
|                            DPDP COMPLIANCE LIFECYCLE                              |
+-----------------------------------------------------------------------------------+
|  1. Notice & Consent    --> Granular, unbundled checkboxes per verification task  |
|  2. Cryptographic Chain --> Append-only SHA-256 hash ledger of all granted receipts |
|  3. In-Memory Extraction--> OCR processes specimen image strictly in volatile RAM  |
|  4. Immediate Purge     --> Specimen images deleted immediately post-validation   |
|  5. Masked Logging      --> PII masked in all DB logs (37XXXXXXXXXXXZS)           |
+-----------------------------------------------------------------------------------+
```

---

## 2. Granular, Unbundled Purpose Specification

In accordance with DPDP Section 6(1), consent is collected with explicit, granular notice prior to document processing:

1. **Enterprise Identity Verification (Required):**
   - *Purpose:* Verifying commercial registration standing against GSTN and Ministry of MSME Udyam registries.
   - *Legal basis:* Performance of commercial contract.
2. **Premises Installation Feasibility (Required):**
   - *Purpose:* Verifying registered business address coordinates to validate telecom tower line-of-sight and fiber distribution terminals.
3. **Signatory Authority Audit (Required):**
   - *Purpose:* Verifying that the individual placing the enterprise order possesses documented legal authority (Owner / Partner / Director) to bind the commercial entity.
4. **Service Alerts & Upgrades (Optional):**
   - *Purpose:* Opt-in WhatsApp network status notifications. Can be unchecked without obstructing connectivity onboarding.

---

## 3. Cryptographic Tamper-Evident Consent Ledger

Consent events are recorded in an append-only, tamper-evident hash chain stored in the `consent` table:

$$\text{hash}_n = \text{SHA-256}\left(\text{hash}_{n-1} + \text{journey\_id} + \text{purposes\_json} + \text{notice\_version} + \text{timestamp}\right)$$

- Any post-facto modification or deletion of past consent records breaks the cryptographic hash continuity and triggers immediate alerts in the compliance audit logs.
- Verified in backend tests by `test_consent_ledger_tampering_breaks_hash`.

---

## 4. Zero-Retention Image Policy & Auto-Purge TTL

Specimen documents (Aadhaar cards, utility bills, GST certificates) carry high privacy risks:

1. **Extraction in Memory:** Documents uploaded via `/api/kyc/upload` are processed in ephemeral memory.
2. **Immediate Deletion:** Once fields are extracted, cross-checked against government registries, and hashed, the raw image bytes are purged from disk.
3. **Retention of Minimised Artifacts Only:**
   - Document SHA-256 hash (to prevent duplicate submissions).
   - Extracted text fields (minimised to business name, address, and masked numbers).
   - Timestamp and deterministic rule evaluation verdict.
4. **Automated Background Purge (`UPLOAD_TTL_MINUTES=30`):** Any orphaned temporary file older than 30 minutes in `./tmp_uploads` is scrubbed automatically by `services/privacy.py`.

---

## 5. PII Masking Standards

- **GSTIN & PAN Masking:** The middle 11 characters of PAN/GSTIN are masked in all audit trails and UI logs (`37XXXXXXXXXXXZS`).
- **Aadhaar Masking:** Aadhaar numbers are masked to the last 4 digits only (`XXXXXXXX1234`).
- **No Raw Identifiers in Application Logs:** All telemetry events (`AppEvent`) reference internal UUIDs rather than raw customer identifiers.
