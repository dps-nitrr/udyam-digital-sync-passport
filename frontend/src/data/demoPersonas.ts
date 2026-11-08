export interface DemoPersona {
  id: string;
  name: string;
  tag: string;
  identifier: string;
  type: "gstin" | "udyam";
  lang: "en" | "hi";
  expectedSegment: string;
  description: string;
  expectedBehavior: string;
}

export interface DemoKycFixture {
  id: string;
  applicant: string;
  expectedVerdict: "pass" | "review" | "fail";
  summary: string;
  plantedIssue?: string;
}

export const DEMO_PERSONAS: DemoPersona[] = [
  {
    id: "D1",
    name: "D1: Active Retailer",
    tag: "Micro Retail",
    identifier: "19EOGXH4115Y1ZL",
    type: "gstin",
    lang: "en",
    expectedSegment: "Micro retail & services",
    description: "Suresh Provision & General Store (West Bengal) — Active GSTIN",
    expectedBehavior: "Zero-touch lookup, starter AirFiber + POS + WhatsApp API recommended"
  },
  {
    id: "D2",
    name: "D2: No GST (Udyam Only)",
    tag: "GST-Free Starter",
    identifier: "UDYAM-WB-00-5053330",
    type: "udyam",
    lang: "hi",
    expectedSegment: "Micro retail & services",
    description: "Maa Tara Sweets — Micro enterprise with valid Udyam registration",
    expectedBehavior: "Udyam verified in Hindi, recommends GST-free AirFiber starter (P04)"
  },
  {
    id: "D3",
    name: "D3: Dental Clinic",
    tag: "Professional Office",
    identifier: "32TTNXB7384T1ZW",
    type: "gstin",
    lang: "en",
    expectedSegment: "Professional offices",
    description: "Balaji Dental Care LLP (Kerala) — Healthcare practice",
    expectedBehavior: "Infers Professional Office, recommends Symmetric Fibre + Cloud Backup + Domain Workspace"
  },
  {
    id: "D4",
    name: "D4: Multi-Site Food Chain",
    tag: "5-Site Enterprise",
    identifier: "19JENXB8672I1ZA",
    type: "gstin",
    lang: "en",
    expectedSegment: "Small multi-site businesses",
    description: "Blue Lotus Kitchens Pvt Ltd (West Bengal) — Restaurant chain with 5 locations",
    expectedBehavior: "Infers multi-site, recommends 24m term, branch failover + managed Wi-Fi per store"
  },
  {
    id: "D5",
    name: "D5: Furniture Manufacturer",
    tag: "Manufacturer",
    identifier: "27XUIXG0767D1ZP",
    type: "gstin",
    lang: "en",
    expectedSegment: "Small manufacturers",
    description: "Ganesh Woodcraft (Maharashtra) — 20-employee workshop",
    expectedBehavior: "Infers Small Manufacturer, recommends Leased Line + Hardware Firewall + 24m contract"
  },
  {
    id: "D6",
    name: "D6: Cancelled GSTIN",
    tag: "Compliance Alert",
    identifier: "37IHKXV5167L1ZS",
    type: "gstin",
    lang: "en",
    expectedSegment: "Micro retail & services",
    description: "Krishna Enterprises (Andhra Pradesh) — GSTIN is Cancelled",
    expectedBehavior: "Flags gst_status_issue alert, routes strictly to GST-free starter without crashing"
  }
];

export const DEMO_KYC_FIXTURES: DemoKycFixture[] = [
  { id: "K01", applicant: "Anil Kumar (K01)", expectedVerdict: "fail", summary: "Planted Cancelled GSTIN in registry cross-check", plantedIssue: "GSTIN Status is Cancelled in mock registry" },
  { id: "K02", applicant: "Babita Sharma (K02)", expectedVerdict: "pass", summary: "Monospace 0 vs O substitution corrected automatically", plantedIssue: "OCR confusion resolved by registry match" },
  { id: "K03", applicant: "Chetan Verma (K03)", expectedVerdict: "pass", summary: "Clean proprietor retail onboarding with valid docs" },
  { id: "K04", applicant: "Deepa Nair (K04)", expectedVerdict: "pass", summary: "Clean healthcare clinic verification" },
  { id: "K05", applicant: "Eshwar Rao (K05)", expectedVerdict: "pass", summary: "Clean multi-site chain compliance" },
  { id: "K06", applicant: "Farida Khan (K06)", expectedVerdict: "pass", summary: "Monospace 8 vs 5 substitution corrected automatically", plantedIssue: "OCR confusion resolved by registry match" },
  { id: "K07", applicant: "Gopal Joshi (K07)", expectedVerdict: "fail", summary: "Signatory name mismatch against GST signatory", plantedIssue: "Aadhaar name doesn't match registry signatory" },
  { id: "K08", applicant: "Harish Gupta (K08)", expectedVerdict: "pass", summary: "Clean industrial manufacturer submission" },
  { id: "K09", applicant: "Indira Sen (K09)", expectedVerdict: "pass", summary: "Clean micro retail submission" },
  { id: "K10", applicant: "Javed Akhtar (K10)", expectedVerdict: "review", summary: "Signatory designation is 'Manager', triggers review", plantedIssue: "Non-owner signatory authority needs confirmation" },
  { id: "K11", applicant: "Kavita Pillai (K11)", expectedVerdict: "fail", summary: "Address utility bill dated 2025-10-31 (>90 days old)", plantedIssue: "Utility bill expired (257 days old relative to demo date)" },
  { id: "K12", applicant: "Lalit Modi (K12)", expectedVerdict: "pass", summary: "Clean small retail enterprise submission" }
];
