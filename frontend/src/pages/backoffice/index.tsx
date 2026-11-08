import React, { useState } from 'react';
import { Leads } from './Leads';
import { Dashboard } from './Dashboard';
import { Users, BarChart3, ArrowLeft } from 'lucide-react';
import { useJourneyStore } from '../../store/journey';

export const Backoffice: React.FC = () => {
  const [tab, setTab] = useState<'leads' | 'dashboard'>('leads');
  const { setStep } = useJourneyStore();

  return (
    <div className="w-full max-w-5xl mx-auto px-4 py-6 space-y-4">
      {/* Top Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <button
            onClick={() => setStep('ENTRY')}
            className="text-xs font-bold text-brand hover:underline inline-flex items-center space-x-1 mb-1"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Return to Customer Onboarding App</span>
          </button>
          <h1 className="text-xl font-black text-graphite-dark tracking-tight">
            Advisor &amp; Partner Back-Office Console
          </h1>
          <p className="text-xs text-graphite-light">
            AI-driven propensity scoring, digital triage, and partner dispatch
          </p>
        </div>

        {/* Tab Toggle */}
        <div className="flex items-center bg-slate-200/80 p-1 rounded-xl">
          <button
            onClick={() => setTab('leads')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              tab === 'leads'
                ? 'bg-white text-graphite-dark shadow-xs'
                : 'text-slate-600 hover:text-graphite-dark'
            }`}
          >
            <Users className="w-3.5 h-3.5 text-brand" />
            <span>Unclosed Leads Triage</span>
          </button>

          <button
            onClick={() => setTab('dashboard')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              tab === 'dashboard'
                ? 'bg-white text-graphite-dark shadow-xs'
                : 'text-slate-600 hover:text-graphite-dark'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5 text-brand" />
            <span>Funnel Analytics</span>
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {tab === 'leads' ? <Leads /> : <Dashboard />}
    </div>
  );
};
