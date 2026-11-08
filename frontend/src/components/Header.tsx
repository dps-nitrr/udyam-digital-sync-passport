import React from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { Globe, RefreshCw, BarChart3, Smartphone } from 'lucide-react';

export const Header: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { language, setLanguage, currentStep, setStep, resetJourney, demoMode } = useJourneyStore();

  const toggleLanguage = () => {
    const next = language === 'en' ? 'hi' : 'en';
    setLanguage(next);
    i18n.changeLanguage(next);
  };

  const isBackoffice = currentStep === 'BACKOFFICE';

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 px-4 py-3 shadow-sm">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        {/* Wordmark (Strictly text wordmark per branding spec, NO trademark logos) */}
        <div
          onClick={() => setStep('ENTRY')}
          className="flex items-center space-x-2 cursor-pointer select-none"
        >
          <div className="w-8 h-8 rounded-lg bg-brand flex items-center justify-center text-white font-black text-lg shadow-sm">
            A
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-graphite-dark text-lg leading-tight tracking-tight">
              Accel <span className="text-brand">Business</span>
            </span>
            <span className="text-[10px] text-graphite-light font-medium tracking-wider uppercase">
              Sync Passport
            </span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-2">
          {/* Demo mode badge */}
          {demoMode && (
            <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-100 text-amber-800 border border-amber-300">
              Demo Active (?demo=1)
            </span>
          )}

          {/* Portal Switcher: Backoffice vs Customer Flow */}
          <button
            onClick={() => setStep(isBackoffice ? 'ENTRY' : 'BACKOFFICE')}
            className={`flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              isBackoffice
                ? 'bg-brand text-white hover:bg-brand-dark'
                : 'bg-slate-100 text-graphite-dark hover:bg-slate-200'
            }`}
            title={isBackoffice ? 'Switch to Customer App' : 'Switch to Back-Office Console'}
          >
            {isBackoffice ? (
              <>
                <Smartphone className="w-3.5 h-3.5" />
                <span className="hidden xs:inline">Customer App</span>
              </>
            ) : (
              <>
                <BarChart3 className="w-3.5 h-3.5" />
                <span className="hidden xs:inline">Back-Office</span>
              </>
            )}
          </button>

          {/* Language Toggle */}
          <button
            onClick={toggleLanguage}
            className="flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-graphite-dark hover:bg-slate-200 transition-colors"
            title="Toggle Language / भाषा बदलें"
          >
            <Globe className="w-3.5 h-3.5 text-brand" />
            <span>{language === 'en' ? 'हिंदी' : 'English'}</span>
          </button>

          {/* Reset Journey */}
          <button
            onClick={resetJourney}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            title="Reset Demo Journey"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
