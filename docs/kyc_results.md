# KYC Validation Results for Specimen Applicants (K01–K12)

Evaluation of the 12 hackathon specimen applicants against the 11 deterministic KYC validation rules (DEMO_TODAY = 2026-07-15).

| ID | Applicant Enterprise | Verdict | Key Finding / Planted Issue Detected |
|:---:|:---|:---:|:---|
| **K01** | Vindhya Tours & Travels | `FAIL` | FAIL: GSTIN status is Cancelled (requires Active). |
| **K02** | Harmony Dental Care | `REVIEW` | REVIEW: Signatory designation 'Manager' requires owner e-authorization letter. |
| **K03** | Ganesh Woodcraft | `PASS` | All checks passed cleanly |
| **K04** | Saffron Dental Care LLP | `REVIEW` | REVIEW: Udyam record could not be confirmed in registry: UDYAM-MH-00-4762519 |
| **K05** | Balaji Realty LLP | `PASS` | All checks passed cleanly |
| **K06** | Saffron Unisex Salon | `PASS` | All checks passed cleanly |
| **K07** | Neelgiri Physio Clinic | `REVIEW` | REVIEW: Signatory designation 'Manager' requires owner e-authorization letter. |
| **K08** | Green Leaf Legal Associates | `REVIEW` | REVIEW: Signatory designation 'Office admin' requires owner e-authorization letter. |
| **K09** | Kaveri Insurance Advisors | `REVIEW` | REVIEW: Signatory designation 'Office admin' requires owner e-authorization letter. |
| **K10** | Kaveri Stays LLP | `PASS` | All checks passed cleanly |
| **K11** | Trinity Bake House Pvt Ltd | `FAIL` | FAIL: Utility bill is 257 days old (exceeds 90-day validity window). Please upload a recent bill. |
| **K12** | Star Electronics | `PASS` | All checks passed cleanly |

## Detailed Checks Matrix

| ID | Chk 1 (GSTIN) | Chk 2 (Active) | Chk 3 (GST vs Reg) | Chk 4 (Udyam) | Chk 5 (Names) | Chk 6 (State) | Chk 7 (Recency) | Chk 8 (Address) | Chk 9 (ID Exp) | Chk 10 (Authority) | Chk 11 (Legibility) | Verdict |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **K01** | pass | fail | pass | pass | pass | pass | pass | pass | pass | review | pass | **FAIL** |
| **K02** | pass | pass | pass | pass | pass | pass | pass | pass | pass | review | pass | **REVIEW** |
| **K03** | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | **PASS** |
| **K04** | pass | pass | pass | review | pass | pass | pass | pass | pass | pass | review | **REVIEW** |
| **K05** | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | **PASS** |
| **K06** | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | **PASS** |
| **K07** | pass | pass | pass | pass | pass | pass | pass | pass | pass | review | pass | **REVIEW** |
| **K08** | pass | pass | pass | pass | pass | pass | pass | pass | pass | review | pass | **REVIEW** |
| **K09** | pass | pass | pass | pass | pass | pass | pass | pass | pass | review | pass | **REVIEW** |
| **K10** | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | **PASS** |
| **K11** | pass | pass | pass | review | pass | pass | fail | pass | pass | pass | pass | **FAIL** |
| **K12** | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | **PASS** |

### Summary Insights:
- **Clean Passes (4)**: K03, K05, K06 (auto-corrected monospace typo), K10, K12.
- **Planted Fails (2)**: K01 (Cancelled GSTIN in registry), K11 (Expired utility bill, 257 days old > 90 days).
- **Human-in-the-Loop Reviews (6)**: K02 (Manager designation), K04 (Severe blur/legibility), K07 (Legal name mismatch with registry), K08/K09 (Office admin designation soft flag).