import React from 'react';
import { useJourneyStore } from '../store/journey';
import { DEMO_PERSONAS, DEMO_KYC_FIXTURES } from '../data/demoPersonas';
import { api } from '../api/client';
import { Sparkles, FileCheck2, AlertCircle } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface DemoBarProps {
  onSelectPersona?: (identifier: string, lang: 'en' | 'hi') => void;
  onLoadKycFixture?: (fixtureId: string) => void;
}

export const DemoBar: React.FC<DemoBarProps> = ({ onSelectPersona, onLoadKycFixture }) => {
  const { demoMode, currentStep, setStep, journeyId, setKycResults } = useJourneyStore();
  const { i18n } = useTranslation();

  if (!demoMode) return null;

  const handleSelectPersona = (p: typeof DEMO_PERSONAS[0]) => {
    if (onSelectPersona) {
      onSelectPersona(p.identifier, p.lang);
    }
  };

  const handleQuickKyc = async (fixtureId: string) => {
    if (onLoadKycFixture) {
      onLoadKycFixture(fixtureId);
      return;
    }
    if (!journeyId) {
      alert('Please start a journey first by entering or clicking a persona above.');
      return;
    }
    try {
      const res = await api.loadKycSpecimen(journeyId, fixtureId);
      setKycResults({
        overallVerdict: res.overall_verdict,
        checks: res.checks,
        nextAction: res.next_action,
      });
      setStep('KYC');
    } catch (err: any) {
      alert(`Error loading fixture: ${err.message}`);
    }
  };

  return (
    <div className="bg-slate-900 text-white text-xs border-b border-slate-700 px-3 py-2 z-30 shadow-md">
      <div className="max-w-4xl mx-auto space-y-2">
        {/* Row 1: Personas */}
        <div className="flex items-center space-x-2 overflow-x-auto pb-1 scrollbar-thin">
          <div className="flex items-center space-x-1 shrink-0 text-amber-400 font-bold tracking-wider uppercase text-[10px]">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Judge Demo Pre-fills:</span>
          </div>
          <div className="flex items-center space-x-1.5 shrink-0">
            {DEMO_PERSONAS.map((p) => (
              <button
                key={p.id}
                onClick={() => handleSelectPersona(p)}
                className="px-2.5 py-1 rounded bg-slate-800 hover:bg-brand text-slate-200 hover:text-white border border-slate-700 hover:border-brand transition-all flex items-center space-x-1"
                title={`${p.description} — ${p.expectedBehavior}`}
              >
                <span className="font-semibold text-amber-300">{p.id}</span>
                <span className="text-slate-300">({p.tag})</span>
              </button>
            ))}
          </div>
        </div>

        {/* Row 2: KYC Fixtures (Shown especially on KYC or general) */}
        <div className="flex items-center space-x-2 overflow-x-auto pb-0.5 scrollbar-thin border-t border-slate-800 pt-1.5">
          <div className="flex items-center space-x-1 shrink-0 text-cyan-400 font-bold tracking-wider uppercase text-[10px]">
            <FileCheck2 className="w-3.5 h-3.5" />
            <span>KYC Fixtures (K01-K12):</span>
          </div>
          <div className="flex items-center space-x-1 shrink-0">
            {DEMO_KYC_FIXTURES.map((k) => {
              const badgeColor =
                k.expectedVerdict === 'pass'
                  ? 'border-green-600/50 hover:bg-green-950 text-green-300'
                  : k.expectedVerdict === 'review'
                  ? 'border-amber-600/50 hover:bg-amber-950 text-amber-300'
                  : 'border-rose-600/50 hover:bg-rose-950 text-rose-300';
              return (
                <button
                  key={k.id}
                  onClick={() => handleQuickKyc(k.id)}
                  className={`px-2 py-0.5 rounded bg-slate-800/80 border text-[11px] font-medium transition-all ${badgeColor}`}
                  title={`${k.applicant} — Expected: ${k.expectedVerdict.toUpperCase()} (${k.summary})`}
                >
                  {k.id} {k.expectedVerdict === 'fail' ? '❌' : k.expectedVerdict === 'review' ? '⚠️' : '✅'}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
