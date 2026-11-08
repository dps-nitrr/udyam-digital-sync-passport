import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { api } from '../api/client';
import { DEMO_KYC_FIXTURES } from '../data/demoPersonas';
import {
  UploadCloud,
  FileCheck,
  CheckCircle2,
  AlertTriangle,
  AlertOctagon,
  ArrowRight,
  Share2,
  Sparkles,
  ShieldAlert,
  Lock,
} from 'lucide-react';

export const Kyc: React.FC = () => {
  const { t } = useTranslation();
  const {
    journeyId,
    business,
    kycResults,
    setKycResults,
    setOrder,
    setStep,
    demoMode,
  } = useJourneyStore();

  const [loading, setLoading] = useState(false);
  const [selectedFixture, setSelectedFixture] = useState<string>('K03');
  const [showRemoteSignModal, setShowRemoteSignModal] = useState(false);
  const [remoteLinkCopied, setRemoteLinkCopied] = useState(false);

  const handleFileUpload = async (docType: string, e: React.ChangeEvent<HTMLInputElement>) => {
    if (!journeyId || !e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setLoading(true);

    try {
      await api.uploadKycDoc(journeyId, docType, file);
      // Run finalize to get latest checks
      const finalRes = await api.finalizeKyc(journeyId);
      setKycResults({
        overallVerdict: finalRes.overall_verdict,
        checks: finalRes.details,
        nextAction: finalRes.next_action,
      });
    } catch (err: any) {
      alert(`Upload error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadFixture = async (fixtureId: string) => {
    if (!journeyId) return;
    setLoading(true);
    setSelectedFixture(fixtureId);
    try {
      const res = await api.loadKycSpecimen(journeyId, fixtureId);
      setKycResults({
        overallVerdict: res.overall_verdict,
        checks: res.checks,
        nextAction: res.next_action,
      });
    } catch (err: any) {
      alert(`Fixture load failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleProceedToOrder = async () => {
    if (!journeyId) return;
    setLoading(true);
    try {
      const orderRes = await api.createOrder(journeyId);
      const statusRes = await api.getOrderStatus(orderRes.order_id);
      setOrder(statusRes);
      setStep('TRACKER');
    } catch (err: any) {
      alert(`Order creation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const isPassed = kycResults?.overallVerdict === 'pass';
  const isReview = kycResults?.overallVerdict === 'review';
  const isFail = kycResults?.overallVerdict === 'fail';

  return (
    <div className="w-full max-w-mobile mx-auto px-4 py-5 space-y-4">
      {/* Title */}
      <div className="text-center space-y-1">
        <h2 className="text-xl font-black text-graphite-dark tracking-tight">
          {t('kyc.title')}
        </h2>
        <p className="text-xs text-graphite-light">
          {t('kyc.subtitle')}
        </p>
      </div>

      {/* Demo Specimen Pre-attach Bar */}
      {demoMode && (
        <div className="p-3 bg-slate-900 rounded-2xl border border-slate-700 text-white space-y-2">
          <div className="flex items-center justify-between text-xs font-bold text-amber-400">
            <span className="flex items-center space-x-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Judge Specimen Quick Loader:</span>
            </span>
            <span className="text-[10px] text-slate-400 font-mono">1-Click Attach</span>
          </div>
          <div className="grid grid-cols-4 gap-1.5">
            {DEMO_KYC_FIXTURES.slice(0, 8).map((fix) => (
              <button
                key={fix.id}
                onClick={() => handleLoadFixture(fix.id)}
                disabled={loading}
                className={`py-1 px-1.5 rounded text-[11px] font-bold border transition-all ${
                  selectedFixture === fix.id
                    ? 'bg-amber-400 text-slate-950 border-amber-300'
                    : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                }`}
                title={fix.summary}
              >
                {fix.id} {fix.expectedVerdict === 'fail' ? '❌' : fix.expectedVerdict === 'review' ? '⚠️' : '✅'}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 4 Document Upload Cards */}
      <div className="grid grid-cols-2 gap-2.5">
        {/* Doc 1: GST / Udyam */}
        <label className="p-3 bg-white rounded-xl border border-slate-200 shadow-2xs hover:border-brand cursor-pointer flex flex-col justify-between space-y-2 text-xs transition-colors">
          <div className="flex items-center justify-between">
            <FileCheck className="w-4 h-4 text-brand" />
            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-slate-100 text-graphite-dark">
              Req
            </span>
          </div>
          <div>
            <span className="font-bold text-graphite-dark block">
              {t('kyc.docGst')}
            </span>
            <span className="text-[10px] text-graphite-light block mt-0.5">
              Registration proof
            </span>
          </div>
          <input
            type="file"
            accept="image/*,application/pdf"
            onChange={(e) => handleFileUpload('gst_cert', e)}
            className="hidden"
          />
        </label>

        {/* Doc 2: Signatory ID */}
        <label className="p-3 bg-white rounded-xl border border-slate-200 shadow-2xs hover:border-brand cursor-pointer flex flex-col justify-between space-y-2 text-xs transition-colors">
          <div className="flex items-center justify-between">
            <FileCheck className="w-4 h-4 text-brand" />
            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-slate-100 text-graphite-dark">
              Req
            </span>
          </div>
          <div>
            <span className="font-bold text-graphite-dark block">
              {t('kyc.docSignatory')}
            </span>
            <span className="text-[10px] text-graphite-light block mt-0.5">
              PAN / Aadhaar card
            </span>
          </div>
          <input
            type="file"
            accept="image/*,application/pdf"
            onChange={(e) => handleFileUpload('signatory_id', e)}
            className="hidden"
          />
        </label>

        {/* Doc 3: Address Proof */}
        <label className="p-3 bg-white rounded-xl border border-slate-200 shadow-2xs hover:border-brand cursor-pointer flex flex-col justify-between space-y-2 text-xs transition-colors">
          <div className="flex items-center justify-between">
            <FileCheck className="w-4 h-4 text-brand" />
            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-slate-100 text-graphite-dark">
              Req
            </span>
          </div>
          <div>
            <span className="font-bold text-graphite-dark block">
              {t('kyc.docAddress')}
            </span>
            <span className="text-[10px] text-graphite-light block mt-0.5">
              Bill &lt; 90 days old
            </span>
          </div>
          <input
            type="file"
            accept="image/*,application/pdf"
            onChange={(e) => handleFileUpload('address_proof', e)}
            className="hidden"
          />
        </label>

        {/* Doc 4: Letter of Authority */}
        <label className="p-3 bg-white rounded-xl border border-slate-200 shadow-2xs hover:border-brand cursor-pointer flex flex-col justify-between space-y-2 text-xs transition-colors">
          <div className="flex items-center justify-between">
            <FileCheck className="w-4 h-4 text-slate-400" />
            <span className="text-[10px] font-semibold px-1.5 py-0.2 rounded bg-slate-100 text-slate-500">
              Opt
            </span>
          </div>
          <div>
            <span className="font-bold text-graphite-dark block">
              {t('kyc.docAuthority')}
            </span>
            <span className="text-[10px] text-graphite-light block mt-0.5">
              For Company / LLP
            </span>
          </div>
          <input
            type="file"
            accept="image/*,application/pdf"
            onChange={(e) => handleFileUpload('board_resolution', e)}
            className="hidden"
          />
        </label>
      </div>

      {/* Remote Sign Trigger Link */}
      <div className="text-center">
        <button
          onClick={() => setShowRemoteSignModal(true)}
          className="text-xs font-bold text-brand hover:underline inline-flex items-center space-x-1"
        >
          <Share2 className="w-3.5 h-3.5" />
          <span>{t('kyc.sendLink')}</span>
        </button>
      </div>

      {/* Remote Signing Simulation Modal */}
      {showRemoteSignModal && (
        <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full p-5 space-y-3 text-xs shadow-xl">
            <h3 className="font-extrabold text-sm text-graphite-dark">
              Remote Document Signing Link
            </h3>
            <p className="text-graphite-light leading-relaxed">
              If you are an advisor or employee applying on behalf of the business owner, share this secure WhatsApp / SMS link for them to complete biometric Aadhaar e-sign.
            </p>
            <div className="p-2.5 bg-slate-100 rounded-lg font-mono text-[11px] text-slate-700 truncate">
              https://sync.accel.biz/sign/{journeyId?.slice(0, 8)}
            </div>
            <button
              onClick={() => {
                setRemoteLinkCopied(true);
                setTimeout(() => {
                  setRemoteLinkCopied(false);
                  setShowRemoteSignModal(false);
                }, 1500);
              }}
              className="w-full py-2.5 bg-brand text-white font-bold rounded-xl"
            >
              {remoteLinkCopied ? 'Link Copied to Clipboard!' : 'Copy Secure Link'}
            </button>
            <button
              onClick={() => setShowRemoteSignModal(false)}
              className="w-full py-2 text-slate-500 font-semibold"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* 11-Rule Deterministic Compliance Checklist */}
      {kycResults && kycResults.checks && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 space-y-3 text-xs">
          {/* Header Verdict Ribbon */}
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <span className="font-black text-xs text-graphite-dark uppercase tracking-wider">
              {t('kyc.checklistTitle')}
            </span>
            <span
              className={`px-2.5 py-1 rounded-full text-xs font-black uppercase tracking-wider flex items-center space-x-1 ${
                isPassed
                  ? 'bg-green-100 text-success border border-green-200'
                  : isReview
                  ? 'bg-amber-100 text-warn border border-amber-200'
                  : 'bg-red-100 text-danger border border-red-300 font-extrabold'
              }`}
            >
              {isPassed ? (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>{t('kyc.pass')}</span>
                </>
              ) : isReview ? (
                <>
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>{t('kyc.review')}</span>
                </>
              ) : (
                <>
                  <AlertOctagon className="w-3.5 h-3.5" />
                  <span>{t('kyc.fail')}</span>
                </>
              )}
            </span>
          </div>

          {/* Next Action Instructions */}
          {kycResults.nextAction && (
            <div
              className={`p-2.5 rounded-xl text-[11px] font-medium leading-relaxed ${
                isPassed
                  ? 'bg-green-50 text-green-900 border border-green-200'
                  : isReview
                  ? 'bg-amber-50 text-amber-900 border border-amber-200'
                  : 'bg-red-50 text-danger border border-red-200'
              }`}
            >
              {kycResults.nextAction}
            </div>
          )}

          {/* Checks List */}
          <div className="space-y-1.5 max-h-60 overflow-y-auto pr-1">
            {kycResults.checks.map((c, i) => (
              <div
                key={i}
                className="flex items-start justify-between py-1.5 border-b border-slate-50 text-[11px]"
              >
                <div className="flex items-start space-x-2 flex-1 pr-2">
                  {c.passed ? (
                    <CheckCircle2 className="w-4 h-4 text-success shrink-0 mt-0.5" />
                  ) : c.severity === 'review' ? (
                    <AlertTriangle className="w-4 h-4 text-warn shrink-0 mt-0.5" />
                  ) : (
                    <AlertOctagon className="w-4 h-4 text-danger shrink-0 mt-0.5" />
                  )}
                  <div>
                    <span className="font-bold text-graphite-dark block">
                      {c.name}
                    </span>
                    <span className="text-[10px] text-graphite-light leading-snug">
                      {c.details}
                    </span>
                  </div>
                </div>

                <span
                  className={`text-[9px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded ${
                    c.passed
                      ? 'bg-green-50 text-success'
                      : c.severity === 'review'
                      ? 'bg-amber-50 text-warn'
                      : 'bg-red-50 text-danger'
                  }`}
                >
                  {c.passed ? 'PASS' : c.severity === 'review' ? 'REVIEW' : 'FAIL'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Proceed CTA */}
      <button
        onClick={handleProceedToOrder}
        disabled={loading || isFail}
        className="w-full py-4 px-4 rounded-xl bg-brand hover:bg-brand-dark text-white font-extrabold text-sm shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2"
      >
        <span>{t('kyc.btnContinue')}</span>
        <ArrowRight className="w-4 h-4" />
      </button>
    </div>
  );
};
