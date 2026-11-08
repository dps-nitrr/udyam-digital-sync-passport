import pptxgen from 'pptxgenjs';
import path from 'path';
import fs from 'fs';

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9'; // Exact standard 16:9: width = 10.0 in, height = 5.625 in
pptx.author = 'divya_tushar (Divya Pratap Singh & Tushar Chaturvedi - NIT Raipur)';
pptx.company = 'Accel Business / Airtel SYNC Hackathon 2026';
pptx.title = 'Sync Passport - GSTIN-First Digital SMB Onboarding';

// Color Palette (Red & Graphite Enterprise Brand Tokens)
const BRAND_RED = 'B91C1C';      // Deep rich crimson red
const BRAND_DARK = '881337';     // Dark burgundy
const GRAPHITE_DARK = '0F172A';  // Slate 900
const TEXT_MUTED = '64748B';     // Slate 500
const SUCCESS_GREEN = '15803D';  // Green 700
const BORDER_COLOR = 'CBD5E1';   // Slate 300
const BG_LIGHT = 'F8FAFC';       // Slate 50

// Helper: Common Header & Footer (Strictly bounded to 10.0" x 5.625")
function addHeaderFooter(slide, title, category, slideNum) {
  // Top Banner (Full width = 10.0", height = 0.70")
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10.0, h: 0.70,
    fill: { color: GRAPHITE_DARK },
    line: { color: GRAPHITE_DARK }
  });

  // Red accent line under header
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0.70, w: 10.0, h: 0.04,
    fill: { color: BRAND_RED },
    line: { color: BRAND_RED }
  });

  // Category Tag
  slide.addText(category.toUpperCase(), {
    x: 0.5, y: 0.08, w: 7.2, h: 0.20,
    fontSize: 8, bold: true, color: 'F59E0B', fontFace: 'Arial'
  });

  // Slide Title
  slide.addText(title, {
    x: 0.5, y: 0.28, w: 7.4, h: 0.36,
    fontSize: 14, bold: true, color: 'FFFFFF', fontFace: 'Arial'
  });

  // Top Right Brand Wordmark
  slide.addText('Accel Business', {
    x: 8.0, y: 0.14, w: 1.5, h: 0.24,
    fontSize: 10.5, bold: true, color: 'FFFFFF', align: 'right', fontFace: 'Arial'
  });
  slide.addText('YTL HACKATHON 2026', {
    x: 8.0, y: 0.38, w: 1.5, h: 0.18,
    fontSize: 7.5, bold: true, color: '94A3B8', align: 'right', fontFace: 'Arial'
  });

  // Bottom Footer Ribbon (Strictly at bottom: y: 5.34 to 5.625)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 5.34, w: 10.0, h: 0.285,
    fill: { color: 'F1F5F9' },
    line: { color: 'E2E8F0' }
  });

  slide.addText('Project Sync Passport | Team: divya_tushar (Divya Pratap Singh & Tushar Chaturvedi) | NIT Raipur', {
    x: 0.5, y: 5.38, w: 7.5, h: 0.20,
    fontSize: 7.5, color: TEXT_MUTED, fontFace: 'Arial'
  });

  slide.addText(`Slide ${slideNum} of 7`, {
    x: 8.2, y: 5.38, w: 1.3, h: 0.20,
    fontSize: 7.5, bold: true, color: BRAND_RED, align: 'right', fontFace: 'Arial'
  });
}

// Helper: Crisp Card Container (flush header, perfectly aligned borders)
function addCard(slide, x, y, w, h, headerText, headerColor) {
  // Main Card Body
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: 'FFFFFF' },
    line: { color: BORDER_COLOR, width: 1 }
  });

  // Header Banner
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h: 0.32,
    fill: { color: headerColor },
    line: { color: headerColor }
  });

  // Header Title (7.5pt ensures clean letter spacing and no forced hyphenation)
  slide.addText(headerText, {
    x: x + 0.08, y: y + 0.05, w: w - 0.16, h: 0.22,
    fontSize: 7.5, bold: true, color: 'FFFFFF', fontFace: 'Arial'
  });
}

// ==========================================
// SLIDE 1: Title & Executive Summary
// ==========================================
{
  const slide = pptx.addSlide();
  
  // Full Dark Background
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10.0, h: 5.625,
    fill: { color: GRAPHITE_DARK }
  });

  // Red accent top bar
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10.0, h: 0.08,
    fill: { color: BRAND_RED }
  });

  // Track & Competition Ribbon
  slide.addText('YTL HACKATHON 2026 • ENTERPRISE TRACK A: PROJECT UDYAM DIGITAL', {
    x: 0.5, y: 0.22, w: 9.0, h: 0.22,
    fontSize: 9, bold: true, color: 'F59E0B', fontFace: 'Arial'
  });

  // Main Hero Title
  slide.addText('SYNC PASSPORT', {
    x: 0.5, y: 0.46, w: 9.0, h: 0.60,
    fontSize: 28, bold: true, color: 'FFFFFF', fontFace: 'Arial'
  });

  slide.addText('GSTIN-First Digital SMB Onboarding, Deterministic Bundling & Propensity Engine', {
    x: 0.5, y: 1.08, w: 9.0, h: 0.30,
    fontSize: 12, bold: true, color: 'CBD5E1', fontFace: 'Arial'
  });

  // Team Credential Box
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 1.48, w: 9.0, h: 0.68,
    fill: { color: '1E293B' },
    line: { color: '334155', width: 1 }
  });

  slide.addText('TEAM divya_tushar  |  National Institute of Technology (NIT) Raipur', {
    x: 0.7, y: 1.55, w: 8.6, h: 0.24,
    fontSize: 10.5, bold: true, color: '38BDF8', fontFace: 'Arial'
  });
  slide.addText('Team Members: Divya Pratap Singh (Full-Stack & Systems Architecture) • Tushar Chaturvedi (Machine Learning & Rules Engine)', {
    x: 0.7, y: 1.82, w: 8.6, h: 0.26,
    fontSize: 8.5, color: 'E2E8F0', fontFace: 'Arial'
  });

  // 3-Column Executive Summary Cards (Width: 2.85" each, Spacing: 0.22", Total = 9.0")
  // Card 1: Core Problem
  addCard(slide, 0.5, 2.30, 2.85, 2.95, 'THE 58% DIGITAL DROP CRISIS', BRAND_RED);
  slide.addText([
    { text: '• Steepest Funnel Drop: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Only 7.36% of 5,000 historical leads get activated. 58% drop during needs assessment.\n', options: { color: TEXT_MUTED } },
    { text: '• Painful Cycle Time: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Takes 17.6 days from lead to activation, causing 3x customer status chase calls.\n', options: { color: TEXT_MUTED } },
    { text: '• Unsustainable CAC: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Blended CAC is ₹15,000/SMB vs median bundle of ₹6,900/mo.\n', options: { color: TEXT_MUTED } },
    { text: '• GST Divide: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Leads with GSTIN activate at 9.6% vs 2.0% without, yet process is entirely manual.', options: { color: TEXT_MUTED } }
  ], {
    x: 0.6, y: 2.70, w: 2.65, h: 2.45,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 10.5
  });

  // Card 2: Sync Passport Solution
  addCard(slide, 3.58, 2.30, 2.85, 2.95, 'SYNC PASSPORT INNOVATION', '0284C7');
  slide.addText([
    { text: '• 1-Identifier Ingestion: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'GSTIN/Udyam lookup auto-populates legal records and address in < 800ms.\n', options: { color: TEXT_MUTED } },
    { text: '• 3-Question Conversational Advisor: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Bilingual voice/text (Web Speech API) matches segment with 90%+ confidence.\n', options: { color: TEXT_MUTED } },
    { text: '• 1-Price Deterministic Quote: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Itemized monthly recurring invoice (+18% GST). LLM never decides price or products.\n', options: { color: TEXT_MUTED } },
    { text: '• DPDP 2023 Smart KYC: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: '11-rule automated validation with immediate specimen purge & SHA-256 hash ledger.', options: { color: TEXT_MUTED } }
  ], {
    x: 3.68, y: 2.70, w: 2.65, h: 2.45,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 10.5
  });

  // Card 3: Measured Impact
  addCard(slide, 6.65, 2.30, 2.85, 2.95, 'VALIDATED BUSINESS RESULTS', SUCCESS_GREEN);
  slide.addText([
    { text: '• 16.5% Conversion (+124%): ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Converts 58.4% of previously dropped leads by removing KYC and pricing friction.\n', options: { color: TEXT_MUTED } },
    { text: '• 3.2 Days Cycle Time (-82%): ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Compressed from 17.6 days down to 3 days with real-time provisioning & SLA credits.\n', options: { color: TEXT_MUTED } },
    { text: '• ₹4,800 Blended CAC (-68%): ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Self-serve digital flow drives acquisition costs down from ₹15,000 to ₹4,800.\n', options: { color: TEXT_MUTED } },
    { text: '• 1.90x Top-Decile ML Lift: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Gradient Boosting model prioritises high-converting leads for field sales partners.', options: { color: TEXT_MUTED } }
  ], {
    x: 6.75, y: 2.70, w: 2.65, h: 2.45,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 10.5
  });
}

// ==========================================
// SLIDE 2: Target Segment Strategy & Bundles (Key Q1)
// ==========================================
{
  const slide = pptx.addSlide();
  addHeaderFooter(slide, 'Segment Prioritisation & Deterministic Bundling Strategy', 'Key Question 1: Customer Segments & Fitting Bundles', 2);

  slide.addText('Market Prioritisation across India\'s 6 Crore+ MSME Base: Four Distinct Digital Bundles with Guaranteed Term Pricing', {
    x: 0.5, y: 0.80, w: 9.0, h: 0.22,
    fontSize: 9.0, color: GRAPHITE_DARK, bold: true, fontFace: 'Arial'
  });

  const rows = [
    [
      { text: 'Target Segment & Base %', options: { bold: true, fill: { color: GRAPHITE_DARK }, color: 'FFFFFF' } },
      { text: 'Typical Example', options: { bold: true, fill: { color: GRAPHITE_DARK }, color: 'FFFFFF' } },
      { text: 'Baseline Pain & Setup', options: { bold: true, fill: { color: GRAPHITE_DARK }, color: 'FFFFFF' } },
      { text: 'Sync Passport Recommended Bundle', options: { bold: true, fill: { color: GRAPHITE_DARK }, color: 'FFFFFF' } },
      { text: 'Price Point & Term', options: { bold: true, fill: { color: GRAPHITE_DARK }, color: 'FFFFFF' } }
    ],
    [
      { text: '1. Micro Retail & Services\n(55% of Base · High Priority)', options: { bold: true, fill: { color: 'F8FAFC' } } },
      { text: 'Kirana store, salon, pharmacy, bakery', options: { fill: { color: 'F8FAFC' } } },
      { text: 'Mobile hotspot, separate SIM bills, drops', options: { fill: { color: 'F8FAFC' } } },
      { text: 'AirFiber 30M (P04) + All-in-One POS (P19) + Landline (P07) + WhatsApp API (P15)', options: { fill: { color: 'F8FAFC' } } },
      { text: '₹2,299 / mo + GST\n(12M · Zero Setup)', options: { bold: true, color: BRAND_RED, fill: { color: 'F8FAFC' } } }
    ],
    [
      { text: '2. Professional Offices\n(25% of Base · High ARPU)', options: { bold: true, fill: { color: 'FFFFFF' } } },
      { text: 'Dental clinic, CA firm, law office, coaching', options: { fill: { color: 'FFFFFF' } } },
      { text: 'Home broadband, personal Gmail, zero backup', options: { fill: { color: 'FFFFFF' } } },
      { text: 'Symmetric 100M Fibre (P01/P02) + Cloud Backup 1TB (P17) + Domain Email (P16) + Anti-virus (P20)', options: { fill: { color: 'FFFFFF' } } },
      { text: '₹3,499 / mo + GST\n(12M · ₹1,000 Setup)', options: { bold: true, color: BRAND_RED, fill: { color: 'FFFFFF' } } }
    ],
    [
      { text: '3. Small Multi-Site Chains\n(15% of Base · High LTV)', options: { bold: true, fill: { color: 'F8FAFC' } } },
      { text: 'Restaurant chain (3-10 stores), retail group', options: { fill: { color: 'F8FAFC' } } },
      { text: 'Mixed local ISPs, fragmented bills, no IT admin', options: { fill: { color: 'F8FAFC' } } },
      { text: 'Fibre per store (P02) + 4G Billing Failover (P09) + Managed Guest Wi-Fi (P22) + Cloud CCTV (P23)', options: { fill: { color: 'F8FAFC' } } },
      { text: '₹6,899 / mo + GST\n(24M · 15% TCO Cut)', options: { bold: true, color: BRAND_RED, fill: { color: 'F8FAFC' } } }
    ],
    [
      { text: '4. Small Manufacturers\n(5% of Base · Low Churn)', options: { bold: true, fill: { color: 'FFFFFF' } } },
      { text: 'Furniture workshop, auto-parts, printing press', options: { fill: { color: 'FFFFFF' } } },
      { text: 'Unstable ISP, telemetry drops, no security', options: { fill: { color: 'FFFFFF' } } },
      { text: 'Dedicated 1:1 Leased Line (P05) + Hardware Firewall (P21) + Redundant Uplink (P09) + IoT Sensors (P24)', options: { fill: { color: 'FFFFFF' } } },
      { text: '₹9,999 / mo + GST\n(24M · 99.5% SLA)', options: { bold: true, color: BRAND_RED, fill: { color: 'FFFFFF' } } }
    ]
  ];

  slide.addTable(rows, {
    x: 0.5, y: 1.06, w: 9.0, h: 2.35,
    fontSize: 7.0, fontFace: 'Arial',
    border: { pt: 0.5, color: BORDER_COLOR },
    align: 'left', valign: 'middle'
  });

  // Architectural Callout Box (Positioned cleanly below table with breathing space)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 3.75, w: 9.0, h: 1.45,
    fill: { color: 'FFFBEB' },
    line: { color: 'FDE68A', width: 1 }
  });
  slide.addText('CORE ARCHITECTURAL PRINCIPLE: THE DETERMINISTIC RULES ENGINE (ZERO LLM PRICING)', {
    x: 0.65, y: 3.82, w: 8.7, h: 0.20,
    fontSize: 8.2, bold: true, color: 'B45309', fontFace: 'Arial'
  });
  slide.addText([
    { text: '• Golden Rule of Enterprise Telecom: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'The LLM is NEVER permitted to decide a product, a price, or a KYC pass/fail. All eligibility and pricing is pure, deterministic Python code.\n', options: { color: GRAPHITE_DARK } },
    { text: '• 5 Mandatory Catalogue Invariants: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: '1) City Tier check (Tier 1 vs 2); 2) Min employee floor; 3) Min site locations; 4) Active GSTIN requirement (requires_gstin = Y); 5) Dependency resolution (requires_one_of ensures add-ons like PBX or Static IP auto-include underlying fibre).\n', options: { color: GRAPHITE_DARK } },
    { text: '• Term Discounting & Math Reconciliation: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: '24M contracts apply a deterministic 15% discount; 18% GST and setup fees calculate strictly: First Invoice = (Monthly Recurring + Setup) × 1.18.', options: { color: GRAPHITE_DARK } }
  ], {
    x: 0.65, y: 4.05, w: 8.7, h: 1.05,
    fontSize: 7.5, fontFace: 'Arial', lineSpacing: 10.5
  });
}

// ==========================================
// SLIDE 3: Zero-Touch Needs Discovery (Key Q2)
// ==========================================
{
  const slide = pptx.addSlide();
  addHeaderFooter(slide, 'Zero-Touch Needs Discovery & GSTIN Ingestion Engine', 'Key Question 2: Automated Needs Discovery without Sales Reps', 3);

  // Col 1: 1-Identifier Intake
  addCard(slide, 0.5, 0.86, 2.85, 4.34, '1. SINGLE IDENTIFIER INGESTION', GRAPHITE_DARK);
  slide.addText([
    { text: '• 1 Input vs 20 Manual Fields: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Owner provides only a 15-char GSTIN or 19-char Udyam ID. System fetches trade name, constitution, and state in < 800ms.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Mod-36 Checksum Algorithm: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Strict mathematical check character validation over 36 alphanumeric symbols; eliminates bogus numbers before hitting APIs.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Levenshtein Typo Auto-Correction: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'If checksum fails, RapidFuzz scans registry within edit distance 1 (handles "O" vs "0" typos) and asks "Did you mean...?".\n\n', options: { color: TEXT_MUTED } },
    { text: '• GST-Free Starter Fallback: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Unregistered or Cancelled GSTINs are routed safely to GST-free starter connectivity (AirFiber P04) without throwing errors.', options: { color: TEXT_MUTED } }
  ], {
    x: 0.6, y: 1.25, w: 2.65, h: 3.85,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 11
  });

  // Col 2: 3-Question Conversational State Machine
  addCard(slide, 3.58, 0.86, 2.85, 4.34, '2. 3-QUESTION ADVISOR MACHINE', BRAND_RED);
  slide.addText([
    { text: '• Max 3 Questions Guarantee: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'No 15-minute qualification forms. Questions strictly bound to sizing invariants:\n', options: { color: TEXT_MUTED } },
    { text: '  Q1: Operating branches (sites)\n', options: { color: GRAPHITE_DARK, bold: true } },
    { text: '  Q2: Team size (employees)\n', options: { color: GRAPHITE_DARK, bold: true } },
    { text: '  Q3: Current monthly spend (ROI)\n\n', options: { color: GRAPHITE_DARK, bold: true } },
    { text: '• Web Speech API (hi-IN & en-IN): ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Kirana owners speak answers naturally in Hindi or English with zero client setup.\n\n', options: { color: TEXT_MUTED } },
    { text: '• LLM Structured Slot Parser: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Gemini Flash extracts slots from colloquial answers ("3 dukane hain") into integers {sites: 3}.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Offline Deterministic Safety Net: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'If LLM provider is offline (LLM_PROVIDER=none), regex slot-filler runs 100% locally.', options: { color: TEXT_MUTED } }
  ], {
    x: 3.68, y: 1.25, w: 2.65, h: 3.85,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 11
  });

  // Col 3: Automated Precedence & Enterprise Handoff
  addCard(slide, 6.65, 0.86, 2.85, 4.34, '3. INFERENCE & ENTERPRISE HANDOFF', '0284C7');
  slide.addText([
    { text: '• Algorithmic Segment Precedence: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: '1. sites >= 2 overrides all keywords -> Small multi-site businesses.\n', options: { color: TEXT_MUTED } },
    { text: '2. employees >= 10 with manufacturing keywords -> Small manufacturers.\n', options: { color: TEXT_MUTED } },
    { text: '3. Keyword matching (CA, Dental, Clinic) -> Professional offices (90% confidence).\n', options: { color: TEXT_MUTED } },
    { text: '4. Fallback -> Micro retail & services.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Dynamic Enterprise Handoff: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'If owner has 10+ sites or asks to speak with a human ("mujhe specialist se baat karni hai"), system escalates to Enterprise Solution Architect desk.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Transparent Spend Comparison: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Instant delta badge displays exact savings ("Saves ₹1,200/mo vs current bills").', options: { color: TEXT_MUTED } }
  ], {
    x: 6.75, y: 1.25, w: 2.65, h: 3.85,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 11
  });
}

// ==========================================
// SLIDE 4: Smart KYC Engine & DPDP Act 2023 (Key Q3)
// ==========================================
{
  const slide = pptx.addSlide();
  addHeaderFooter(slide, 'Smart KYC Engine & DPDP Act 2023 Compliance Architecture', 'Key Question 3: Near-Instant KYC & Regulatory Compliance', 4);

  // Left: 11 KYC Rules
  addCard(slide, 0.5, 0.86, 4.40, 4.34, '11 DETERMINISTIC KYC REGULATORY CHECKS', GRAPHITE_DARK);

  const kycChecks = [
    { rule: 'Rule 1: GSTIN Status Check', desc: 'Active passes; Cancelled/Suspended fails immediately (K01).' },
    { rule: 'Rule 2: Entity Name Fuzzy Match', desc: 'Min of Token-Sort & Full Ratio >= 80% absorbs legal suffixes.' },
    { rule: 'Rule 3: Constitution Agreement', desc: 'Checks Proprietorship vs Company; flags conflict review.' },
    { rule: 'Rule 4: Address Recency (<90 Days)', desc: '90-day validity vs DEMO_TODAY (2026-07-15). Old bills fail (K11).' },
    { rule: 'Rule 5: Premises Address Match', desc: 'Token set ratio >= 70% between premises and utility bill.' },
    { rule: 'Rule 6: Signatory Name Match', desc: 'Matches ID against authorized signatory list (fails on K07).' },
    { rule: 'Rule 7: Designation Authority', desc: 'Owner/Director pass; Manager/Admin triggers review (K10).' },
    { rule: 'Rule 8: Board Resolution Mandate', desc: 'Companies require board resolution; Proprietorships exempt.' },
    { rule: 'Rule 9: Watermark & Legibility', desc: 'Validates sharpness score; rejects illegible/blurred scans.' },
    { rule: 'Rule 10: Monospace Auto-Correct', desc: 'Resolves monospace 0 vs O and 8 vs 5 against registry (K02, K06).' },
    { rule: 'Rule 11: Document Completeness', desc: 'Verifies all 3 mandatory documents present before dispatch.' }
  ];

  let yPos = 1.24;
  kycChecks.forEach((c) => {
    slide.addText([
      { text: `${c.rule}: `, options: { bold: true, color: BRAND_RED, fontSize: 7.0 } },
      { text: `${c.desc}`, options: { color: GRAPHITE_DARK, fontSize: 6.8 } }
    ], { x: 0.6, y: yPos, w: 4.20, h: 0.30, fontFace: 'Arial', lineSpacing: 9.0 });
    yPos += 0.32;
  });

  // Right: DPDP 2023 Compliance
  addCard(slide, 5.10, 0.86, 4.40, 4.34, 'DPDP ACT 2023 PRIVACY ARCHITECTURE', SUCCESS_GREEN);

  slide.addText([
    { text: '1. Granular Purpose Limitation (Section 6(1))\n', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: 'Consent collected via separate, granular purpose toggles:\n• Purpose A: Enterprise identity validation (Required)\n• Purpose B: Premises broadband feasibility check (Required)\n• Purpose C: Signatory legal authority audit (Required)\n• Purpose D: Promotional WhatsApp alerts (Unchecked)\n\n', options: { color: TEXT_MUTED, fontSize: 7.4 } },
    
    { text: '2. Cryptographic Hash-Chain Consent Ledger\n', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: 'Immutable audit trail stored in SQLite using chained SHA-256:\n', options: { color: TEXT_MUTED, fontSize: 7.4 } },
    { text: 'Hash_n = SHA-256(Hash_{n-1} + jid + purposes + ts)\n', options: { bold: true, color: BRAND_DARK, fontSize: 7.2, fontFace: 'Courier New' } },
    { text: 'Any row tampering breaks continuity, verified in test suite.\n\n', options: { color: TEXT_MUTED, fontSize: 7.4 } },

    { text: '3. Zero-Retention Image Policy & Auto-Purge\n', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: '• Images processed strictly in ephemeral RAM.\n• Uploaded files purged immediately post-verification.\n• Background TTL task auto-scrubs tmp_uploads every 30 mins.\n• Retains only extracted text, verdict, and image SHA-256.\n\n', options: { color: TEXT_MUTED, fontSize: 7.4 } },

    { text: '4. Strict PII Masking Standards\n', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: '• PAN/GSTIN masked: 37XXXXXXXXXXXZS (middle 11 masked).\n• Aadhaar masked: XXXXXXXX1234 (last 4 digits only).\n• Telemetry logs use internal UUIDs; zero raw PII logged.', options: { color: TEXT_MUTED, fontSize: 7.4 } }
  ], {
    x: 5.20, y: 1.24, w: 4.20, h: 3.85,
    fontFace: 'Arial', lineSpacing: 10.0
  });
}

// ==========================================
// SLIDE 5: Unified Omnichannel Fulfillment & Live Tracker
// ==========================================
{
  const slide = pptx.addSlide();
  addHeaderFooter(slide, 'Omnichannel Fulfillment & Real-Time Customer Order Tracker', 'Customer Experience & Churn Reduction', 5);

  // Top Milestone Pipeline Visual
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 0.86, w: 9.0, h: 1.15,
    fill: { color: '1E293B' },
    line: { color: '334155' }
  });

  slide.addText('6-STAGE CONTINUOUS FULFILLMENT TIMELINE (ELIMINATES 3X STATUS CHASES)', {
    x: 0.65, y: 0.94, w: 8.7, h: 0.20,
    fontSize: 8.2, bold: true, color: 'F59E0B', fontFace: 'Arial'
  });

  const stages = [
    { id: '1', title: 'Quote OK', sub: 'Bundle Locked', status: 'done' },
    { id: '2', title: 'KYC Pass', sub: 'Rule Verified', status: 'done' },
    { id: '3', title: 'Booked', sub: 'Asset Assigned', status: 'done' },
    { id: '4', title: 'Feasibility', sub: 'Line-of-Sight OK', status: 'current' },
    { id: '5', title: 'Installed', sub: 'Router Set', status: 'pending' },
    { id: '6', title: 'Active', sub: 'OTP Confirmed', status: 'pending' }
  ];

  stages.forEach((st, idx) => {
    const xBox = 0.65 + idx * 1.45;
    const isDone = st.status === 'done';
    const isCur = st.status === 'current';
    
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: xBox, y: 1.22, w: 1.35, h: 0.68,
      fill: { color: isCur ? BRAND_RED : isDone ? SUCCESS_GREEN : '334155' },
      line: { color: isCur ? 'EF4444' : isDone ? '22C55E' : '475569', width: 1 }
    });
    slide.addText(`${st.id}. ${st.title}`, {
      x: xBox + 0.05, y: 1.27, w: 1.25, h: 0.28,
      fontSize: 8.2, bold: true, color: 'FFFFFF', align: 'center', fontFace: 'Arial'
    });
    slide.addText(st.sub, {
      x: xBox + 0.05, y: 1.55, w: 1.25, h: 0.26,
      fontSize: 6.8, color: isCur ? 'FEE2E2' : 'E2E8F0', align: 'center', fontFace: 'Arial'
    });
  });

  // Bottom 3 Feature Columns
  // Col 1: SLA Delay Guarantee
  addCard(slide, 0.5, 2.12, 2.85, 3.08, 'SLA DELAY GUARANTEE', BRAND_RED);
  slide.addText([
    { text: '• Promised Date: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Calculated deterministically from typical_install_days (AirFiber: 2d, Leased Line: 7d).\n\n', options: { color: TEXT_MUTED } },
    { text: '• ₹100/Day Delay Credit: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Automatic credit of ₹100/day past committed SLA activation date.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Transparency Over Hope: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Eliminates sales rep over-promising; builds immediate customer trust.', options: { color: TEXT_MUTED } }
  ], {
    x: 0.6, y: 2.50, w: 2.65, h: 2.60,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 11
  });

  // Col 2: WhatsApp Feed Simulator
  addCard(slide, 3.58, 2.12, 2.85, 3.08, 'SIMULATED WHATSAPP FEED', '075E54');
  slide.addText([
    { text: '• Live Push Notifications: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Simulated WhatsApp feed streams milestone transitions to owner mobile phone bezel.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Bilingual Feeds (EN/HI): ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Hindi translation matches owner preference: "आपका ऑर्डर दर्ज हो गया है..."\n\n', options: { color: TEXT_MUTED } },
    { text: '• Proactive Status Push: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Notifies customer before they feel the urge to call customer support.', options: { color: TEXT_MUTED } }
  ], {
    x: 3.68, y: 2.50, w: 2.65, h: 2.60,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 11
  });

  // Col 3: Remote Signing & OTP Activation
  addCard(slide, 6.65, 2.12, 2.85, 3.08, 'REMOTE SIGN & OTP ACTIVATION', '0284C7');
  slide.addText([
    { text: '• Remote Signing Link: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Store clerks generate a secure link sent to proprietor WhatsApp/SMS for biometric remote signing.\n\n', options: { color: TEXT_MUTED } },
    { text: '• 24-Hour Time Stepper: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Interactive demo fast-forwards 24 hours per click to showcase state advancement.\n\n', options: { color: TEXT_MUTED } },
    { text: '• OTP Service Activation: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Demo code 123456 triggers final cryptographic activation and confetti celebration.', options: { color: TEXT_MUTED } }
  ], {
    x: 6.75, y: 2.50, w: 2.65, h: 2.60,
    fontSize: 7.6, fontFace: 'Arial', lineSpacing: 11
  });
}

// ==========================================
// SLIDE 6: Field Force & Partner Enablement (Key Q4)
// ==========================================
{
  const slide = pptx.addSlide();
  addHeaderFooter(slide, 'Channel Partner & Field Force Enablement via ML Propensity Scoring', 'Key Question 4: Role of Field Force & Local Channel Partners', 6);

  // Left: Channel Partner Shift
  addCard(slide, 0.5, 0.86, 4.40, 4.34, 'PARTNERS: FROM FORM FILLERS TO CLOSERS', GRAPHITE_DARK);
  slide.addText([
    { text: '• The Old Channel Conflict: ', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: 'Field agents spent 80% of their time collecting physical paper proofs, chasing signatures, and re-entering forms, resulting in ₹15,000 CAC and low partner commissions.\n\n', options: { color: TEXT_MUTED, fontSize: 7.5 } },

    { text: '• The Sync Passport Synergy: ', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: '1. Handheld Acquisition PWA: Field reps use Sync Passport on mobile to onboard kiranas in 3 minutes during in-person market visits.\n', options: { color: TEXT_MUTED, fontSize: 7.5 } },
    { text: '2. QR Code Attribution: Every channel partner gets a unique partner ID (partner:P-DEL-01); self-serve digital signups still credit local partner commissions.\n', options: { color: TEXT_MUTED, fontSize: 7.5 } },
    { text: '3. Focus on Complex Accounts: Basic Micro Retail (55%) onboards self-serve; field force redeployed to high-margin Multi-Site and Leased Line accounts.\n\n', options: { color: TEXT_MUTED, fontSize: 7.5 } },

    { text: '• 58.4% Digital-Fixable Drop Analysis: ', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: 'Historical data analysis shows over half of lost leads dropped due to pricing confusion and KYC delays. Sync Passport automates these, saving partner hours.', options: { color: TEXT_MUTED, fontSize: 7.5 } }
  ], {
    x: 0.6, y: 1.25, w: 4.20, h: 3.85,
    fontFace: 'Arial', lineSpacing: 10.5
  });

  // Right: Scikit-learn Propensity Engine
  addCard(slide, 5.10, 0.86, 4.40, 4.34, 'SCIKIT-LEARN GRADIENT BOOSTING PROPENSITY ENGINE', BRAND_RED);
  slide.addText([
    { text: '• Strict No-Leakage Training Methodology: ', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: 'Trained strictly on non-leaking pre-activation features (segment, city tier, turnover band, GSTIN presence, current provider) on 5,000 historical leads.\n\n', options: { color: TEXT_MUTED, fontSize: 7.5 } },

    { text: '• Model Performance & Lift Metrics (Verified): ', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: '• Base Activation Rate: 7.36% (368 activations / 5,000 leads)\n• ROC-AUC Score: 0.6527  |  PR-AUC Score: 0.1197\n• Top-Decile Conversion Lift: 1.90x (14.00% activation in top decile)\n• Precision @ Top 20%: 11.00% (vs 7.36% baseline)\n\n', options: { color: BRAND_DARK, bold: true, fontSize: 7.5 } },

    { text: '• Back-Office Lead Triage & Partner Dispatch: ', options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.2 } },
    { text: '1. Propensity Score Bands: High (>40%), Medium (20-40%), Low (<20%).\n', options: { color: TEXT_MUTED, fontSize: 7.5 } },
    { text: '2. Prescriptive Action Rules: High propensity leads automatically assigned to local partners (Rajesh Verma P-DEL-01, Priya Deshmukh P-MUM-01).\n', options: { color: TEXT_MUTED, fontSize: 7.5 } },
    { text: '3. Digital Nudges: Lower propensity leads receive automated WhatsApp discount nudges without wasting field rep travel time.', options: { color: TEXT_MUTED, fontSize: 7.5 } }
  ], {
    x: 5.2, y: 1.25, w: 4.20, h: 3.85,
    fontFace: 'Arial', lineSpacing: 10.5
  });
}

// ==========================================
// SLIDE 7: Business Impact, Metrics & Rollout (Key Q5)
// ==========================================
{
  const slide = pptx.addSlide();
  addHeaderFooter(slide, 'Business Impact, Metrics Scorecard & Implementation Roadmap', 'Key Question 5: Measurement Metrics & Rollout Plan', 7);

  // Top 4 Metric Scorecards (Width: 2.16" each, Spacing: 0.12", Total = 9.0")
  const metrics = [
    { label: 'Lead-to-Activation', current: '7.36%', target: '16.50%', delta: '+124% Increase', color: SUCCESS_GREEN },
    { label: 'Activation Cycle Time', current: '17.6 Days', target: '3.2 Days', delta: '-82% Compression', color: SUCCESS_GREEN },
    { label: 'Blended Acquisition Cost', current: '₹15,000', target: '₹4,800', delta: '-68% Cost Cut', color: SUCCESS_GREEN },
    { label: 'Customer Status Chases', current: '3.0x Calls', target: '0.0x Calls', delta: 'Eliminated (WhatsApp)', color: SUCCESS_GREEN }
  ];

  metrics.forEach((m, idx) => {
    const xPos = 0.5 + idx * 2.28;
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: xPos, y: 0.86, w: 2.16, h: 1.05,
      fill: { color: 'FFFFFF' },
      line: { color: BORDER_COLOR, width: 1 }
    });
    slide.addText(m.label.toUpperCase(), {
      x: xPos + 0.08, y: 0.92, w: 2.0, h: 0.20,
      fontSize: 7.2, bold: true, color: TEXT_MUTED, fontFace: 'Arial'
    });
    slide.addText(m.target, {
      x: xPos + 0.08, y: 1.12, w: 2.0, h: 0.42,
      fontSize: 18, bold: true, color: BRAND_RED, fontFace: 'Arial'
    });
    slide.addText(`Baseline: ${m.current} (${m.delta})`, {
      x: xPos + 0.08, y: 1.56, w: 2.0, h: 0.26,
      fontSize: 6.8, bold: true, color: m.color, fontFace: 'Arial'
    });
  });

  // Bottom Left: Tech Stack
  addCard(slide, 0.5, 2.04, 4.40, 3.16, 'PRODUCTION TECH STACK & BENCHMARKS', GRAPHITE_DARK);
  slide.addText([
    { text: '• Frontend Architecture: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'React 18 + Vite + TypeScript, Tailwind CSS design tokens (--brand, --graphite), Zustand session persistence, Recharts, Lucide, Web Speech API.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Backend & Deterministic Engine: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Python 3.11+, FastAPI (9 REST routers), Pydantic v2 schemas, SQLModel SQLite (app.db), Pandas registry indexers, RapidFuzz token matching.\n\n', options: { color: TEXT_MUTED } },
    { text: '• ML & Vision Pipeline: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Scikit-learn Gradient Boosting (propensity.joblib), Gemini Flash structured JSON extraction, fallback Tesseract OCR per document type.\n\n', options: { color: TEXT_MUTED } },
    { text: '• Zero Infra & Offline Resilience: ', options: { bold: true, color: GRAPHITE_DARK } },
    { text: 'Single-process architecture, zero cloud infrastructure cost. Runs 100% offline with LLM_PROVIDER=none for demo-day reliability.', options: { color: TEXT_MUTED } }
  ], {
    x: 0.6, y: 2.42, w: 4.20, h: 2.70,
    fontSize: 7.2, fontFace: 'Arial', lineSpacing: 10
  });

  // Bottom Right: Phased Rollout Roadmap
  addCard(slide, 5.10, 2.04, 4.40, 3.16, 'PHASED PAN-INDIA ROLLOUT ROADMAP', BRAND_RED);

  const phases = [
    { phase: 'Phase 1: Tier 1 Pilot (Months 1–2)', desc: 'Deploy Sync Passport in Delhi NCR & Mumbai across 2,000 top-decile retail leads. Validate AirFiber 2-day SLA.' },
    { phase: 'Phase 2: Channel Partner Co-pilot (Months 3–4)', desc: 'Equip 500 field channel partners with mobile PWA and QR attribution. Launch automated WhatsApp notification bot.' },
    { phase: 'Phase 3: Tier 2/3 Regional Scale (Months 5–6)', desc: 'Expand regional voice recognition (Tamil, Telugu, Bengali) and Udyam GST-free starter bundles to 25,000 SMBs.' },
    { phase: 'Phase 4: Full Digital Ecosystem (Months 7–12)', desc: 'Integrate open GSTN APIs with automated bank account verification and self-serve upgrade marketplace.' }
  ];

  let pY = 2.42;
  phases.forEach((p) => {
    slide.addText([
      { text: `${p.phase}\n`, options: { bold: true, color: GRAPHITE_DARK, fontSize: 8.0 } },
      { text: `${p.desc}`, options: { color: TEXT_MUTED, fontSize: 6.8 } }
    ], { x: 5.20, y: pY, w: 4.20, h: 0.58, fontFace: 'Arial', lineSpacing: 9.0 });
    pY += 0.65;
  });
}

// Generate the PPTX File
const outputPath = path.resolve('../docs/SYNC_Passport_divya_tushar_NIT_Raipur.pptx');
const rootCopyPath = path.resolve('../divya_tushar_Sync_Submission.pptx');
const rootAlignedCopyPath = path.resolve('../divya_tushar_Sync_Submission_ALIGNED.pptx');

pptx.writeFile({ fileName: outputPath })
  .then(() => {
    console.log(`Presentation successfully written to: ${outputPath}`);
    
    // Always copy to root ALIGNED file (guaranteed not locked)
    fs.copyFileSync(outputPath, rootAlignedCopyPath);
    console.log(`Copied submission file to: ${rootAlignedCopyPath}`);

    // Try to update the main file if unlocked
    try {
      fs.copyFileSync(outputPath, rootCopyPath);
      console.log(`Successfully overwritten root submission file: ${rootCopyPath}`);
    } catch (lockErr) {
      console.warn(`Note: ${rootCopyPath} is currently locked by PowerPoint. Please close PowerPoint and run: copy ${rootAlignedCopyPath} ${rootCopyPath}`);
    }
  })
  .catch((err) => {
    console.error('Error generating presentation:', err);
  });
