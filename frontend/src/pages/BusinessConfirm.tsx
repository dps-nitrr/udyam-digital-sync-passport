import React from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { Building2, MapPin, FileText, CheckCircle, AlertOctagon, ArrowRight, ArrowLeft, Sparkles } from 'lucide-react';

export const BusinessConfirm: React.FC = () => {
  const { t } = useTranslation();
  const {
    identifier,
    identifierType,
    business,
    segmentGuess,
    gstStatusIssue,
    setStep,
  } = useJourneyStore();

  if (!business) {
    return (
      <div className="w-full max-w-mobile mx-auto px-4 py-8 text-center">
        <p className="text-sm text-graphite-light">No business details found.</p>
        <button
          onClick={() => setStep('ENTRY')}
          className="mt-4 px-4 py-2 bg-brand text-white rounded-lg text-xs font-bold"
        >
          Return to Entry
        </button>
      </div>
    );
  }

  const isActive = business.status?.toLowerCase() === 'active';

  return (
    <div className="w-full max-w-mobile mx-auto px-4 py-6 space-y-4">
      {/* Title */}
      <div className="text-center">
        <h2 className="text-xl font-black text-graphite-dark tracking-tight">
          {t('confirm.title')}
        </h2>
        <p className="text-xs text-graphite-light mt-1">
          {t('confirm.subtitle')} ({identifier})
        </p>
      </div>

      {/* Cancelled / Suspended GST Warning Notice */}
      {gstStatusIssue && (
        <div className="p-3.5 bg-rose-50 rounded-xl border border-rose-300 text-xs text-danger flex items-start space-x-2.5">
          <AlertOctagon className="w-5 h-5 text-danger shrink-0 mt-0.5" />
          <div className="space-y-1">
            <span className="font-bold text-danger uppercase tracking-wide block">
              Compliance Notice: GSTIN is {business.status}
            </span>
            <p className="text-graphite-dark leading-relaxed">
              {t('entry.cancelledWarning')}
            </p>
          </div>
        </div>
      )}

      {/* Main Verified Business Card */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {/* Header Ribbon */}
        <div className="bg-slate-900 text-white px-4 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Building2 className="w-4 h-4 text-amber-400" />
            <span className="text-xs font-bold uppercase tracking-wider">
              {identifierType.toUpperCase()} Record
            </span>
          </div>
          <span
            className={`px-2 py-0.5 rounded text-[11px] font-bold ${
              isActive
                ? 'bg-green-500/20 text-green-300 border border-green-500/40'
                : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
            }`}
          >
            {business.status || 'Verified'}
          </span>
        </div>

        {/* Card Body */}
        <div className="p-4 space-y-3.5 text-xs">
          <div>
            <span className="text-[11px] font-semibold text-graphite-light uppercase tracking-wider block">
              {t('confirm.tradeName')}
            </span>
            <span className="text-base font-extrabold text-graphite-dark block mt-0.5">
              {business.trade_name || business.name}
            </span>
            {business.legal_name && business.legal_name !== business.trade_name && (
              <span className="text-xs text-graphite-light block">
                ({business.legal_name})
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 gap-3 pt-2 border-t border-slate-100">
            <div>
              <span className="text-[11px] font-semibold text-graphite-light uppercase tracking-wider block">
                {t('confirm.constitution')}
              </span>
              <span className="font-bold text-graphite-dark block mt-0.5">
                {business.constitution || business.enterprise_type || 'Commercial Enterprise'}
              </span>
            </div>
            <div>
              <span className="text-[11px] font-semibold text-graphite-light uppercase tracking-wider block">
                State / Jurisdiction
              </span>
              <span className="font-bold text-graphite-dark block mt-0.5">
                {business.state || 'India'}
              </span>
            </div>
          </div>

          {business.address && (
            <div className="pt-2 border-t border-slate-100 flex items-start space-x-1.5 text-graphite-light">
              <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
              <span className="text-[11px] leading-relaxed">{business.address}</span>
            </div>
          )}
        </div>
      </div>

      {/* Inferred Segment Box */}
      {segmentGuess && (
        <div className="bg-amber-50/60 rounded-xl border border-amber-200/80 p-3.5 space-y-1.5">
          <div className="flex items-center space-x-1.5 text-amber-900 font-bold text-xs">
            <Sparkles className="w-4 h-4 text-amber-600" />
            <span>{t('confirm.inferredSegment')}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="font-black text-sm text-graphite-dark">
              {segmentGuess.segment}
            </span>
            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-200/60 text-amber-800">
              {Math.round(segmentGuess.confidence * 100)}% Match
            </span>
          </div>
          <p className="text-[11px] text-amber-800 leading-snug">
            {segmentGuess.reason_display}
          </p>
        </div>
      )}

      {/* Action Buttons */}
      <div className="space-y-2 pt-2">
        <button
          onClick={() => setStep('ADVISOR')}
          className="w-full py-3.5 px-4 rounded-xl bg-brand hover:bg-brand-dark text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center space-x-2"
        >
          <span>{t('confirm.btnConfirm')}</span>
          <ArrowRight className="w-4 h-4" />
        </button>

        <button
          onClick={() => setStep('ENTRY')}
          className="w-full py-2.5 px-4 rounded-xl bg-transparent text-graphite-light hover:text-graphite-dark font-semibold text-xs transition-colors flex items-center justify-center space-x-1"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>{t('confirm.btnEdit')}</span>
        </button>
      </div>
    </div>
  );
};
