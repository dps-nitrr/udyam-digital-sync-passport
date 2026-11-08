import React, { useEffect, useState } from 'react';
import { useJourneyStore } from './store/journey';
import { Header } from './components/Header';
import { DemoBar } from './components/DemoBar';
import { Entry } from './pages/Entry';
import { BusinessConfirm } from './pages/BusinessConfirm';
import { Advisor } from './pages/Advisor';
import { Quote } from './pages/Quote';
import { Consent } from './pages/Consent';
import { Kyc } from './pages/Kyc';
import { Tracker } from './pages/Tracker';
import { Backoffice } from './pages/backoffice';
import './i18n';

export const App: React.FC = () => {
  const { currentStep, setStep, setDemoMode, demoMode, setLanguage } = useJourneyStore();
  const [selectedPersonaIdent, setSelectedPersonaIdent] = useState<string | undefined>();

  useEffect(() => {
    // Detect ?demo=1 in URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('demo') === '1') {
      setDemoMode(true);
    }
  }, []);

  const handleSelectPersona = (ident: string, lang: 'en' | 'hi') => {
    setLanguage(lang);
    setSelectedPersonaIdent(ident);
    setStep('ENTRY');
  };

  const isBackoffice = currentStep === 'BACKOFFICE';

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col justify-between font-sans text-graphite-dark antialiased">
      <div>
        {/* Top Header */}
        <Header />

        {/* Demo Bar (Only when ?demo=1 is active) */}
        <DemoBar
          onSelectPersona={handleSelectPersona}
          onLoadKycFixture={() => setStep('KYC')}
        />

        {/* Main Content Area */}
        <main className={`mx-auto ${isBackoffice ? 'w-full max-w-5xl' : 'w-full max-w-mobile'}`}>
          {currentStep === 'ENTRY' && <Entry prefilledIdentifier={selectedPersonaIdent} />}
          {currentStep === 'CONFIRM' && <BusinessConfirm />}
          {currentStep === 'ADVISOR' && <Advisor />}
          {currentStep === 'QUOTE' && <Quote />}
          {currentStep === 'CONSENT' && <Consent />}
          {currentStep === 'KYC' && <Kyc />}
          {currentStep === 'TRACKER' && <Tracker />}
          {currentStep === 'BACKOFFICE' && <Backoffice />}
        </main>
      </div>

      {/* Footer */}
      <footer className="py-4 text-center text-xs text-graphite-light border-t border-slate-200 bg-white/50 mt-8">
        <div className="max-w-md mx-auto px-4 flex items-center justify-between text-[11px]">
          <span className="font-bold text-graphite-dark">
            Accel Business © 2026
          </span>
          <span className="text-slate-400">
            DPDP 2023 Compliant • SHA-256 Ledger
          </span>
        </div>
      </footer>
    </div>
  );
};

export default App;
