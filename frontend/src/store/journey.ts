import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export type JourneyStep =
  | 'ENTRY'
  | 'CONFIRM'
  | 'ADVISOR'
  | 'QUOTE'
  | 'CONSENT'
  | 'KYC'
  | 'TRACKER'
  | 'BACKOFFICE';

export interface BusinessProfile {
  name: string;
  legal_name?: string;
  trade_name?: string;
  address?: string;
  state?: string;
  city?: string;
  constitution?: string;
  status?: string;
  enterprise_type?: string;
  nic_description?: string;
}

export interface QuoteData {
  quote_id: string;
  term_months: number;
  monthly_recurring: number;
  one_time_setup: number;
  gst_amount: number;
  first_invoice: number;
  tco_term: number;
  vs_current_spend?: number;
  promised_date: string;
  bundle: Array<{
    product_id: string;
    category: string;
    name_plain: string;
    qty: number;
    unit: string;
    unit_price: number;
    line_total: number;
    setup_fee: number;
    why: string;
    min_contract_months: number;
    can_toggle: boolean;
    active: boolean;
  }>;
  excluded: Array<{
    product_id: string;
    product_name: string;
    reason_key: string;
    reason_plain: string;
  }>;
}

export interface KycCheckItem {
  rule_id: string;
  name: string;
  passed: boolean;
  severity: 'fail' | 'review';
  details: string;
}

interface JourneyState {
  language: 'en' | 'hi';
  currentStep: JourneyStep;
  journeyId: string | null;
  identifier: string;
  identifierType: 'gstin' | 'udyam' | 'none';
  business: BusinessProfile | null;
  segment: string | null;
  segmentGuess: any | null;
  gstStatusIssue: boolean;
  advisorQuestions: {
    sites: number;
    employees: number;
    current_spend?: number;
  };
  advisorMessages: Array<{
    sender: 'assistant' | 'user';
    text: string;
  }>;
  quote: QuoteData | null;
  quoteExplanation: string | null;
  consentReceipt: {
    consentId: string;
    hash: string;
    grantedAt: string;
  } | null;
  kycResults: {
    overallVerdict: 'pass' | 'review' | 'fail' | null;
    checks: KycCheckItem[];
    nextAction?: string;
  } | null;
  order: {
    orderId: string | null;
    promisedDate: string | null;
    currentStatus: string;
    history: any[];
    notifications: any[];
  } | null;
  demoMode: boolean;

  // Actions
  setLanguage: (lang: 'en' | 'hi') => void;
  setStep: (step: JourneyStep) => void;
  setJourneyId: (id: string) => void;
  setIdentifier: (ident: string, type?: 'gstin' | 'udyam' | 'none') => void;
  setBusinessData: (
    business: BusinessProfile | null,
    segmentGuess: any | null,
    gstIssue: boolean
  ) => void;
  setAdvisorSlots: (slots: Partial<JourneyState['advisorQuestions']>) => void;
  addAdvisorMessage: (sender: 'assistant' | 'user', text: string) => void;
  setQuote: (quote: QuoteData, explanation?: string) => void;
  setConsentReceipt: (receipt: { consentId: string; hash: string; grantedAt: string }) => void;
  setKycResults: (res: {
    overallVerdict: 'pass' | 'review' | 'fail';
    checks: KycCheckItem[];
    nextAction?: string;
  }) => void;
  setOrder: (order: any) => void;
  setDemoMode: (val: boolean) => void;
  resetJourney: () => void;
}

export const useJourneyStore = create<JourneyState>()(
  persist(
    (set) => ({
      language: 'en',
      currentStep: 'ENTRY',
      journeyId: null,
      identifier: '',
      identifierType: 'gstin',
      business: null,
      segment: null,
      segmentGuess: null,
      gstStatusIssue: false,
      advisorQuestions: {
        sites: 1,
        employees: 2,
      },
      advisorMessages: [],
      quote: null,
      quoteExplanation: null,
      consentReceipt: null,
      kycResults: null,
      order: null,
      demoMode: false,

      setLanguage: (language) => set({ language }),
      setStep: (currentStep) => set({ currentStep }),
      setJourneyId: (journeyId) => set({ journeyId }),
      setIdentifier: (identifier, identifierType = 'gstin') =>
        set({ identifier, identifierType }),
      setBusinessData: (business, segmentGuess, gstStatusIssue) =>
        set({
          business,
          segmentGuess,
          segment: segmentGuess?.segment || null,
          gstStatusIssue,
        }),
      setAdvisorSlots: (slots) =>
        set((state) => ({
          advisorQuestions: { ...state.advisorQuestions, ...slots },
        })),
      addAdvisorMessage: (sender, text) =>
        set((state) => ({
          advisorMessages: [...state.advisorMessages, { sender, text }],
        })),
      setQuote: (quote, quoteExplanation) =>
        set({ quote, quoteExplanation: quoteExplanation || null }),
      setConsentReceipt: (consentReceipt) => set({ consentReceipt }),
      setKycResults: (kycResults) => set({ kycResults }),
      setOrder: (order) => set({ order }),
      setDemoMode: (demoMode) => set({ demoMode }),
      resetJourney: () =>
        set({
          currentStep: 'ENTRY',
          journeyId: null,
          identifier: '',
          identifierType: 'gstin',
          business: null,
          segment: null,
          segmentGuess: null,
          gstStatusIssue: false,
          advisorQuestions: { sites: 1, employees: 2 },
          advisorMessages: [],
          quote: null,
          quoteExplanation: null,
          consentReceipt: null,
          kycResults: null,
          order: null,
        }),
    }),
    {
      name: 'sync-passport-journey',
      storage: createJSONStorage(() => sessionStorage),
    }
  )
);
