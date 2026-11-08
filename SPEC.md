# SPEC.md — "Sync Passport": GSTIN-first SMB onboarding prototype

Read this whole file before writing any code. Build in the order given in Section 17. Do not skip the tests in Section 16.

---

## 0. One-paragraph summary

A mobile-first web app where a small-business owner types or speaks one identifier (GSTIN or Udyam number). The backend looks it up in a mock registry, infers the segment, asks at most 3 confirming questions, recommends a bundle with ONE transparent monthly price, verifies KYC documents (OCR + registry cross-checks) after a clear consent screen, and then shows a live order tracker. A separate back-office console shows leads the advisor could not close, ranked by a propensity score. All business logic (eligibility, price, KYC rules) is **deterministic code**. The LLM is used only to (a) turn free text/voice into structured answers, (b) phrase explanations in the owner's language, (c) read documents as a fallback OCR.

**Golden rule: the LLM never decides a product, a price, or a KYC pass/fail.** Every LLM output is validated against a schema and the catalogue before use. Every LLM call has a deterministic fallback so the demo never breaks.

---

## 1. Context and data (all synthetic, in `/data`)

Copy the contents of `YTL_TrackA_Udyam_Digital_Data.zip` into `/data` unchanged.

| File | Rows | Used for |
|---|---|---|
| `product_catalogue.csv` | 25 | Eligibility, price ranges, setup fees, contract, install days, dependencies |
| `smb_leads.csv` | 5,000 | Propensity model, funnel dashboard, segment lookup, back-office seed |
| `mock_gstin_registry.csv` | 3,534 | GSTIN lookup API. Columns: gstin, legal_name, trade_name, constitution, principal_place_of_business, state, registration_date, status (Active 3,266 / Cancelled 167 / Suspended 101 = 3,534) |
| `mock_udyam_registry.csv` | 2,723 | Udyam lookup API. Columns: udyam_number, enterprise_name, enterprise_type (Micro 1,833 / Small 737 / Medium 153 = 2,723), major_activity, nic_description, state, city, date_of_registration |
| `kyc_documents/` | 47 images | 12 applicants K01-K12, each with GST certificate, Udyam certificate, signatory ID, address proof (some have planted problems) |

Facts that drive the design (from the data; keep them as comments in code where relevant):

- "Today" for all date logic = **2026-07-15** (config `DEMO_TODAY`). Address proof must be no older than 90 days.
- GSTIN has the real 15-char structure with valid checksum. The 4th char of the embedded PAN is always `X` — **accept `X`**.
- Udyam numbers look like `UDYAM-KL-00-3078801` (district code `00`).
- Segments: `Micro retail & services`, `Professional offices`, `Small multi-site businesses`, `Small manufacturers`.
- Catalogue `requires_gstin = Y` products cannot be sold without an Active GSTIN. `requires_one_of` means the bundle must also contain at least one of the listed products.
- Specimen documents have a watermark running across the text and a monospace font where `I`/`1` and `O`/`0` are easy to confuse (see Section 9.3).

---

## 2. Tech stack (fixed — do not substitute)

| Layer | Choice | Reason |
|---|---|---|
| Frontend | React 18 + Vite + TypeScript, Tailwind CSS, Zustand (state), TanStack Query, react-i18next, Recharts, lucide-react | Fast, typed, mobile-first |
| Backend | Python 3.11+, FastAPI, Pydantic v2, SQLModel (SQLite), pandas, rapidfuzz, scikit-learn, pytesseract + Pillow, python-multipart, uvicorn | Data-heavy, single process, zero infra |
| LLM | Behind an `LLMProvider` interface. Default implementation: Gemini via `google-genai` SDK (any current Flash-class model the key supports). Keep the interface so Claude/OpenAI can be swapped in one file. | Needs structured output + vision |
| OCR | Primary: LLM vision returning strict JSON. Fallback: Tesseract + regex per document type | Works offline if API fails |
| Voice (P1) | Browser Web Speech API (`hi-IN`, `en-IN`) | No backend cost |
| Storage | SQLite file `app.db`; uploads in `./tmp_uploads` (auto-purged) | Simple, demoable |
| Tests | pytest (backend), Vitest (frontend rules), one Playwright smoke test (P2) | |

Environment variables (`.env`, with `.env.example` committed):

```
LLM_API_KEY=
LLM_PROVIDER=gemini            # gemini | none  (none = deterministic fallbacks only)
LLM_TIMEOUT_SECONDS=4
DEMO_TODAY=2026-07-15
OTP_DEMO_CODE=123456
UPLOAD_TTL_MINUTES=30
CORS_ORIGIN=http://localhost:5173
```
