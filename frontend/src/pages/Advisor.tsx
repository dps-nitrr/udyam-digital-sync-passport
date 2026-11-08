import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { api } from '../api/client';
import { Bot, User, ArrowRight, Sparkles, AlertCircle, PhoneForwarded } from 'lucide-react';

interface QuestionDef {
  slot: 'sites' | 'employees' | 'current_spend';
  questionKey: string;
  chips: Array<{ label: string; value: number }>;
}

const QUESTIONS: QuestionDef[] = [
  {
    slot: 'sites',
    questionKey: 'How many business locations or branches do you operate?',
    chips: [
      { label: '1 Location (Single Store / Office)', value: 1 },
      { label: '2 Branches', value: 2 },
      { label: '3 - 5 Sites', value: 4 },
      { label: '6 - 9 Locations', value: 6 },
      { label: '10+ Enterprise Footprint', value: 12 },
    ],
  },
  {
    slot: 'employees',
    questionKey: 'How many employees or staff members work across your business?',
    chips: [
      { label: '1 - 4 Members', value: 2 },
      { label: '5 - 9 Staff', value: 6 },
      { label: '10 - 24 Team', value: 15 },
      { label: '25+ Employees', value: 30 },
    ],
  },
  {
    slot: 'current_spend',
    questionKey: 'What is your approximate current monthly telecom & internet bill?',
    chips: [
      { label: 'Under ₹2,000 / mo', value: 1800 },
      { label: '₹2,000 - ₹5,000 / mo', value: 3500 },
      { label: '₹5,000 - ₹10,000 / mo', value: 7500 },
      { label: '₹10,000+ / mo', value: 12000 },
    ],
  },
];

export const Advisor: React.FC = () => {
  const { t, i18n } = useTranslation();
  const {
    language,
    journeyId,
    business,
    segment,
    advisorQuestions,
    setAdvisorSlots,
    setQuote,
    setStep,
  } = useJourneyStore();

  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [handoff, setHandoff] = useState<boolean>(false);
  const [handoffReason, setHandoffReason] = useState<string | null>(null);

  const activeQ = QUESTIONS[currentQIndex];

  const handleSelectChip = async (val: number) => {
    if (!journeyId) return;

    setLoading(true);
    const slot = activeQ.slot;
    setAdvisorSlots({ [slot]: val });

    try {
      const res = await api.sendAdvisorMessage(journeyId, slot, val);

      if (res.handoff) {
        setHandoff(true);
        setHandoffReason(res.handoff_reason || 'Multi-site enterprise requirement');
        setLoading(false);
        return;
      }

      if (currentQIndex < QUESTIONS.length - 1) {
        setCurrentQIndex((prev) => prev + 1);
      } else {
        // All 3 answered -> generate recommendation!
        await handleRecommend();
      }
    } catch (err) {
      console.error(err);
      if (currentQIndex < QUESTIONS.length - 1) {
        setCurrentQIndex((prev) => prev + 1);
      } else {
        await handleRecommend();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRecommend = async () => {
    if (!journeyId) return;
    setLoading(true);
    try {
      const rec = await api.recommendBundle(journeyId);
      setQuote(rec.quote, rec.explanation);
      setStep('QUOTE');
    } catch (err: any) {
      alert(`Recommendation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-mobile mx-auto px-4 py-6 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-200">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center text-brand">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-black text-graphite-dark">
              {t('advisor.title')}
            </h2>
            <span className="text-[11px] text-graphite-light">
              Tailoring for {business?.name || segment || 'Your Business'}
            </span>
          </div>
        </div>
        <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-graphite-dark">
          {t('advisor.step', { current: currentQIndex + 1, total: QUESTIONS.length })}
        </span>
      </div>

      {/* Enterprise Handoff Alert */}
      {handoff && (
        <div className="p-4 bg-amber-50 rounded-2xl border border-amber-300 space-y-3">
          <div className="flex items-center space-x-2 text-amber-900 font-bold text-xs">
            <PhoneForwarded className="w-4 h-4 text-amber-700" />
            <span>Dedicated Enterprise Desk Assigned</span>
          </div>
          <p className="text-xs text-graphite-dark leading-relaxed">
            {handoffReason || t('advisor.handoffAlert')}
          </p>
          <div className="pt-2 flex items-center space-x-2">
            <button
              onClick={handleRecommend}
              className="flex-1 py-2.5 px-3 rounded-xl bg-brand text-white font-bold text-xs"
            >
              Continue to Standard Quote
            </button>
          </div>
        </div>
      )}

      {/* Active Question Bubble */}
      {!handoff && (
        <div className="space-y-4">
          <div className="flex items-start space-x-2.5">
            <div className="w-7 h-7 rounded-full bg-slate-900 flex items-center justify-center text-white shrink-0 mt-0.5">
              <Bot className="w-4 h-4 text-amber-400" />
            </div>
            <div className="p-4 rounded-2xl rounded-tl-none bg-white border border-slate-200 shadow-sm text-xs font-medium text-graphite-dark leading-relaxed">
              <span className="font-extrabold text-sm block mb-1">
                {activeQ.questionKey}
              </span>
              <span className="text-graphite-light">
                This ensures your broadband bandwidth and software licenses are precisely matched.
              </span>
            </div>
          </div>

          {/* Quick Choice Chips */}
          <div className="space-y-2 pt-2">
            <span className="text-[11px] font-bold text-graphite-light uppercase tracking-wider block px-1">
              Select one option:
            </span>
            <div className="grid grid-cols-1 gap-2">
              {activeQ.chips.map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelectChip(chip.value)}
                  disabled={loading}
                  className="w-full text-left p-3.5 rounded-xl border border-slate-200 hover:border-brand hover:bg-red-50/50 bg-white shadow-sm font-semibold text-xs text-graphite-dark transition-all flex items-center justify-between group"
                >
                  <span>{chip.label}</span>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-300 group-hover:text-brand transition-colors" />
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Loading state indicator */}
      {loading && (
        <div className="p-4 text-center space-y-2">
          <div className="inline-flex items-center space-x-2 text-xs font-semibold text-brand">
            <svg className="animate-spin h-4 w-4 text-brand" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
            <span>{t('advisor.typing')}</span>
          </div>
        </div>
      )}
    </div>
  );
};
