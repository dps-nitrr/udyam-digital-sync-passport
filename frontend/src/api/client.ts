const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  const headers = new Headers(options.headers || {});
  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (!res.ok) {
    let errorDetail = 'Request failed';
    try {
      const errJson = await res.json();
      if (Array.isArray(errJson.detail)) {
        errorDetail = errJson.detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ');
      } else if (typeof errJson.detail === 'object' && errJson.detail !== null) {
        errorDetail = JSON.stringify(errJson.detail);
      } else {
        errorDetail = errJson.detail || errJson.message || errorDetail;
      }
    } catch {
      errorDetail = await res.text();
    }
    throw new Error(errorDetail);
  }

  return res.json();
}

export const api = {
  // Journey
  createJourney: (language: string = 'en', source: string = 'self') =>
    request<{ journey_id: string }>('/api/journeys', {
      method: 'POST',
      body: JSON.stringify({ language, source }),
    }),

  // Registry
  lookupRegistry: (journeyId: string, identifier: string) =>
    request<{
      identifier_type: string;
      valid_format: boolean;
      checksum_ok: boolean;
      found: boolean;
      status?: string;
      business?: {
        name: string;
        trade_name?: string;
        legal_name?: string;
        address?: string;
        state?: string;
        city?: string;
        constitution?: string;
        status?: string;
        enterprise_type?: string;
        nic_description?: string;
      };
      segment_guess?: {
        segment: string;
        confidence: number;
        reason_key: string;
        reason_display: string;
      };
      suggestion?: string;
      gst_status_issue: boolean;
    }>('/api/registry/lookup', {
      method: 'POST',
      body: JSON.stringify({ journey_id: journeyId, identifier }),
    }),

  // Advisor
  sendAdvisorMessage: (
    journeyId: string,
    slot?: string,
    chipValue?: any,
    text?: string
  ) =>
    request<{
      next_state: string;
      assistant_message: string;
      chips: Array<{ label: string; value: any }>;
      slots_filled: Record<string, any>;
      handoff: boolean;
      handoff_reason?: string;
      llm_used: boolean;
    }>('/api/advisor/message', {
      method: 'POST',
      body: JSON.stringify({ journey_id: journeyId, slot, chip_value: chipValue, text }),
    }),

  recommendBundle: (journeyId: string) =>
    request<{
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
      quote: {
        quote_id: string;
        term_months: number;
        monthly_recurring: number;
        one_time_setup: number;
        gst_amount: number;
        first_invoice: number;
        tco_term: number;
        vs_current_spend?: number;
        promised_date: string;
        bundle: any[];
        excluded: Array<{
          product_id: string;
          product_name: string;
          reason_key: string;
          reason_plain: string;
        }>;
      };
      explanation: string;
      llm_used: boolean;
    }>('/api/advisor/recommend', {
      method: 'POST',
      body: JSON.stringify({ journey_id: journeyId }),
    }),

  // Quote
  updateQuote: (
    journeyId: string,
    termMonths?: number,
    quantities?: Record<string, number>,
    toggles?: Record<string, boolean>
  ) =>
    request<{
      quote: {
        quote_id: string;
        term_months: number;
        monthly_recurring: number;
        one_time_setup: number;
        gst_amount: number;
        first_invoice: number;
        tco_term: number;
        vs_current_spend?: number;
        promised_date: string;
        bundle: any[];
        excluded: any[];
      };
      auto_added: string[];
      auto_removed: string[];
    }>('/api/quote/update', {
      method: 'POST',
      body: JSON.stringify({
        journey_id: journeyId,
        term_months: termMonths,
        quantities,
        toggles,
      }),
    }),

  acceptQuote: (journeyId: string) =>
    request<{ quote_id: string; accepted_at: string; status: string }>(
      '/api/quote/accept',
      {
        method: 'POST',
        body: JSON.stringify({ journey_id: journeyId }),
      }
    ),

  // Consent
  submitConsent: (
    journeyId: string,
    acceptedPurposes: string[],
    noticeVersion: string = 'v1.0'
  ) =>
    request<{
      consent_id: string;
      granted_at: string;
      hash: string;
      prev_hash: string;
    }>('/api/consent', {
      method: 'POST',
      body: JSON.stringify({
        journey_id: journeyId,
        accepted_purposes: acceptedPurposes,
        notice_version: noticeVersion,
      }),
    }),

  // KYC
  uploadKycDoc: (journeyId: string, docType: string, file: File) => {
    const fd = new FormData();
    fd.append('journey_id', journeyId);
    fd.append('doc_type', docType);
    fd.append('file', file);
    return request<{
      check_id: string;
      doc_type: string;
      extracted: Record<string, any>;
      checks: Array<{
        rule_id: string;
        name: string;
        passed: boolean;
        severity: 'fail' | 'review';
        details: string;
      }>;
      verdict: 'pass' | 'review' | 'fail';
      message: string;
    }>('/api/kyc/upload', {
      method: 'POST',
      body: fd,
    });
  },

  loadKycSpecimen: (journeyId: string, fixtureId: string) =>
    request<{
      fixture_id: string;
      overall_verdict: 'pass' | 'review' | 'fail';
      docs_loaded: string[];
      extracted_data: Record<string, any>;
      next_action: string;
      checks: Array<{
        rule_id: string;
        name: string;
        passed: boolean;
        severity: 'fail' | 'review';
        details: string;
      }>;
    }>('/api/kyc/load-specimen', {
      method: 'POST',
      body: JSON.stringify({ journey_id: journeyId, fixture_id: fixtureId }),
    }),

  finalizeKyc: (journeyId: string) =>
    request<{
      overall_verdict: 'pass' | 'review' | 'fail';
      missing: string[];
      next_action: string;
      details: Array<{
        rule_id: string;
        name: string;
        passed: boolean;
        severity: 'fail' | 'review';
        details: string;
      }>;
    }>('/api/kyc/finalize', {
      method: 'POST',
      body: JSON.stringify({ journey_id: journeyId }),
    }),

  // Orders & Tracker
  createOrder: (journeyId: string) =>
    request<{ order_id: string; promised_date: string }>('/api/orders', {
      method: 'POST',
      body: JSON.stringify({ journey_id: journeyId }),
    }),

  getOrderStatus: (orderId: string) =>
    request<{
      order_id: string;
      current_status: string;
      promised_date: string;
      days_to_promised: number;
      history: Array<{
        status: string;
        message: string;
        timestamp: string;
      }>;
      notifications: Array<{
        channel: string;
        body: string;
        timestamp: string;
      }>;
    }>(`/api/orders/${orderId}`),

  simulateAdvanceOrder: (orderId: string, days: number = 1) =>
    request<{
      order_id: string;
      current_status: string;
      promised_date: string;
      days_to_promised: number;
      history: any[];
      notifications: any[];
    }>(`/api/orders/${orderId}/simulate-advance`, {
      method: 'POST',
      body: JSON.stringify({ days }),
    }),

  requestOtp: (phone: string = '9876543210') =>
    request<{ status: string; message: string }>('/api/auth/otp/request', {
      method: 'POST',
      body: JSON.stringify({ phone }),
    }),

  verifyOtp: (code: string, phone: string = '9876543210') =>
    request<{ valid: boolean; token: string }>('/api/auth/otp/verify', {
      method: 'POST',
      body: JSON.stringify({ code, phone }),
    }),

  // Back-office
  getBackofficeLeads: (params?: { segment?: string; outcome?: string; min_score?: number }) => {
    const qs = new URLSearchParams();
    if (params?.segment) qs.set('segment', params.segment);
    if (params?.outcome) qs.set('outcome', params.outcome);
    if (params?.min_score) qs.set('min_score', params.min_score.toString());
    return request<{
      leads: Array<{
        lead_id: string;
        business_name: string;
        segment: string;
        city: string;
        state: string;
        stage_reached: string;
        outcome: string;
        drop_reason: string;
        propensity_score: number;
        priority_band: 'High' | 'Medium' | 'Low';
        recommended_action: string;
        top_factors: string[];
        assigned_partner?: string;
      }>;
      total: number;
    }>(`/api/backoffice/leads?${qs.toString()}`);
  },

  getFunnelMetrics: () =>
    request<{
      funnel: Array<{ stage: string; count: number; drop_rate: number }>;
      kpis: {
        total_leads: number;
        conversion_rate: number;
        avg_cycle_days: number;
        digital_fixable_drops: number;
      };
      drop_reasons: Array<{ reason: string; count: number; fixable: boolean }>;
    }>('/api/backoffice/funnel'),

  assignPartner: (leadId: string, partnerId: string) =>
    request<{ status: string; assigned_to: string }>('/api/backoffice/assign', {
      method: 'POST',
      body: JSON.stringify({ lead_id: leadId, partner_id: partnerId }),
    }),
};
