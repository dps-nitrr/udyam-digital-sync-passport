import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { api } from '../api/client';
import { ShieldCheck, Lock, FileKey, CheckSquare, Square, ArrowRight, ArrowLeft } from 'lucide-react';

export const Consent: React.FC = () => {
  const { t } = useTranslation();
  const { journeyId, setConsentReceipt, setStep } = useJourneyStore();

  const [marketingConsent, setMarketingConsent] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmitConsent = async () => {
    if (!journeyId) return;

    setLoading(true);
    const acceptedPurposes = [
      'verify_identity',
      'verify_address',
      'verify_signatory',
      ...(marketingConsent ? ['marketing_alerts'] : []),
    ];

    try {
      const res = await api.submitConsent(journeyId, acceptedPurposes);
      setConsentReceipt({
        consentId: res.consent_id,
        hash: res.hash,
        grantedAt: res.granted_at,
      });
      setStep('KYC');
    } catch (err: any) {
      alert(`Consent recording failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-mobile mx-auto px-4 py-6 space-y-4">
      {/* Title */}
      <div className="text-center space-y-1">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-slate-900 text-white text-xs font-semibold mb-1 shadow-xs">
          <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
          <span>DPDP Act 2023 Compliant</span>
        </div>
        <h2 className="text-xl font-black text-graphite-dark tracking-tight">
          {t('consent.title')}
        </h2>
        <p className="text-xs text-graphite-light">
          {t('consent.subtitle')}
        </p>
      </div>

      {/* Main Consent Form Card */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-4 text-xs">
        <div>
          <span className="font-extrabold text-graphite-dark block text-xs uppercase tracking-wider mb-2">
            {t('consent.purposeTitle')}
          </span>

          <div className="space-y-2.5">
            {/* Purpose 1 (Required) */}
            <div className="flex items-start space-x-2.5 p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-graphite-dark">
              <CheckSquare className="w-4 h-4 text-brand shrink-0 mt-0.5" />
              <div className="flex-1">
                <span className="font-bold text-graphite-dark block">
                  1. Enterprise Registry Verification
                </span>
                <span className="text-[11px] text-graphite-light leading-snug block mt-0.5">
                  Cross-checks applicant details against GSTN and Udyam database.
                </span>
              </div>
              <span className="text-[10px] font-bold text-brand uppercase tracking-wider">
                Required
              </span>
            </div>

            {/* Purpose 2 (Required) */}
            <div className="flex items-start space-x-2.5 p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-graphite-dark">
              <CheckSquare className="w-4 h-4 text-brand shrink-0 mt-0.5" />
              <div className="flex-1">
                <span className="font-bold text-graphite-dark block">
                  2. Installation Address Feasibility
                </span>
                <span className="text-[11px] text-graphite-light leading-snug block mt-0.5">
                  Validates operational site coordinates and telecom tower line-of-sight.
                </span>
              </div>
              <span className="text-[10px] font-bold text-brand uppercase tracking-wider">
                Required
              </span>
            </div>

            {/* Purpose 3 (Required) */}
            <div className="flex items-start space-x-2.5 p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-graphite-dark">
              <CheckSquare className="w-4 h-4 text-brand shrink-0 mt-0.5" />
              <div className="flex-1">
                <span className="font-bold text-graphite-dark block">
                  3. Signatory Authority Audit
                </span>
                <span className="text-[11px] text-graphite-light leading-snug block mt-0.5">
                  Confirms authorized signatory authority on behalf of the commercial entity.
                </span>
              </div>
              <span className="text-[10px] font-bold text-brand uppercase tracking-wider">
                Required
              </span>
            </div>

            {/* Purpose 4 (Optional) */}
            <div
              onClick={() => setMarketingConsent(!marketingConsent)}
              className="flex items-start space-x-2.5 p-2.5 bg-white rounded-xl border border-slate-200 text-graphite-dark cursor-pointer hover:bg-slate-50 transition-colors"
            >
              {marketingConsent ? (
                <CheckSquare className="w-4 h-4 text-brand shrink-0 mt-0.5" />
              ) : (
                <Square className="w-4 h-4 text-slate-300 shrink-0 mt-0.5" />
              )}
              <div className="flex-1">
                <span className="font-bold text-graphite-dark block">
                  4. Service Alerts & Speed Upgrades
                </span>
                <span className="text-[11px] text-graphite-light leading-snug block mt-0.5">
                  Optional WhatsApp updates regarding network maintenance and new features.
                </span>
              </div>
              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
                Optional
              </span>
            </div>
          </div>
        </div>

        {/* DPDP Zero-Retention Policy Notice */}
        <div className="p-3 bg-red-50/60 rounded-xl border border-red-100 flex items-start space-x-2 text-[11px] text-graphite-dark leading-relaxed">
          <Lock className="w-4 h-4 text-brand shrink-0 mt-0.5" />
          <span>{t('consent.retentionNote')}</span>
        </div>

        {/* Cryptographic Hash Ledger Receipt Preview */}
        <div className="p-3 bg-slate-900 rounded-xl border border-slate-700 text-slate-300 space-y-1 font-mono text-[10px]">
          <div className="flex items-center space-x-1 text-amber-400 font-bold uppercase tracking-wider">
            <FileKey className="w-3.5 h-3.5" />
            <span>Immutable Hash-Chain Receipt:</span>
          </div>
          <p className="text-slate-400 truncate">
            sha256(prev_hash + purposes + timestamp)
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="space-y-2 pt-2">
        <button
          onClick={handleSubmitConsent}
          disabled={loading}
          className="w-full py-4 px-4 rounded-xl bg-brand hover:bg-brand-dark text-white font-extrabold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center space-x-2"
        >
          <span>{t('consent.btnConsent')}</span>
          <ArrowRight className="w-4 h-4" />
        </button>

        <button
          onClick={() => setStep('QUOTE')}
          className="w-full py-2.5 px-4 rounded-xl bg-transparent text-graphite-light hover:text-graphite-dark font-semibold text-xs transition-colors flex items-center justify-center space-x-1"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Quote</span>
        </button>
      </div>
    </div>
  );
};
