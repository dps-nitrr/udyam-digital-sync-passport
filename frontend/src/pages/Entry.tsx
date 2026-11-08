import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { api } from '../api/client';
import { Search, Mic, MicOff, AlertTriangle, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';

interface EntryProps {
  prefilledIdentifier?: string;
}

export const Entry: React.FC<EntryProps> = ({ prefilledIdentifier }) => {
  const { t, i18n } = useTranslation();
  const {
    language,
    journeyId,
    setJourneyId,
    setIdentifier,
    setBusinessData,
    setStep,
  } = useJourneyStore();

  const [inputVal, setInputVal] = useState(prefilledIdentifier || '');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [suggestion, setSuggestion] = useState<string | null>(null);
  const [cancelledIssue, setCancelledIssue] = useState<boolean>(false);
  const [isListening, setIsListening] = useState<boolean>(false);

  // Sync if prefilled from DemoBar
  useEffect(() => {
    if (prefilledIdentifier) {
      setInputVal(prefilledIdentifier);
      handleLookup(prefilledIdentifier);
    }
  }, [prefilledIdentifier]);

  // Voice Search using Web Speech API
  const handleVoiceInput = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(t('entry.speechError'));
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === 'hi' ? 'hi-IN' : 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    setIsListening(true);
    recognition.start();

    recognition.onresult = (event: any) => {
      const speechResult = event.results[0][0].transcript.trim().toUpperCase().replace(/\s+/g, '');
      setInputVal(speechResult);
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
      setErrorMsg(t('entry.speechError'));
    };

    recognition.onend = () => {
      setIsListening(false);
    };
  };

  const handleLookup = async (identToUse?: string) => {
    const ident = (identToUse || inputVal).trim().toUpperCase();
    if (!ident) {
      setErrorMsg('Please enter a valid GSTIN or Udyam number.');
      return;
    }

    setLoading(true);
    setErrorMsg(null);
    setSuggestion(null);
    setCancelledIssue(false);

    try {
      // 1. Ensure Journey exists
      let activeJourneyId = journeyId;
      if (!activeJourneyId) {
        const jRes = await api.createJourney(language);
        activeJourneyId = jRes.journey_id;
        setJourneyId(activeJourneyId);
      }

      // 2. Perform Registry Lookup
      const res = await api.lookupRegistry(activeJourneyId, ident);

      if (!res.found) {
        if (res.suggestion) {
          setSuggestion(res.suggestion);
          setErrorMsg(`Identifier not found in registry. Did you mean ${res.suggestion}?`);
        } else {
          setErrorMsg(
            'Identifier not found in mock registry. Please verify or use one of our demo presets above.'
          );
        }
        setLoading(false);
        return;
      }

      // 3. Save to Store
      setIdentifier(ident, res.identifier_type as any);
      setBusinessData(res.business || null, res.segment_guess || null, res.gst_status_issue);

      if (res.gst_status_issue) {
        setCancelledIssue(true);
      }

      // 4. Navigate to Confirmation
      setStep('CONFIRM');
    } catch (err: any) {
      setErrorMsg(err.message || 'Lookup failed. Please check network connection.');
    } finally {
      setLoading(false);
    }
  };

  const handleNoGstPath = () => {
    setInputVal('UDYAM-WB-00-5053330');
    handleLookup('UDYAM-WB-00-5053330');
  };

  return (
    <div className="w-full max-w-mobile mx-auto px-4 py-6">
      {/* Hero Welcome */}
      <div className="text-center mb-6">
        <div className="inline-flex items-center space-x-1 px-3 py-1 rounded-full bg-red-50 text-brand text-xs font-semibold mb-3 border border-red-100">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Government Registry Verified</span>
        </div>
        <h1 className="text-2xl font-black text-graphite-dark tracking-tight leading-snug">
          {t('entry.title')}
        </h1>
        <p className="text-sm text-graphite-light mt-1.5 leading-relaxed">
          {t('entry.subtitle')}
        </p>
      </div>

      {/* Main Identifier Card */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 space-y-4">
        <div>
          <label className="block text-xs font-bold text-graphite-dark uppercase tracking-wider mb-2">
            {t('entry.inputLabel')}
          </label>
          <div className="relative flex items-center">
            <input
              type="text"
              value={inputVal}
              onChange={(e) => {
                setInputVal(e.target.value);
                setErrorMsg(null);
                setSuggestion(null);
              }}
              placeholder={t('entry.placeholder')}
              className="w-full px-4 py-3.5 pr-12 rounded-xl border border-slate-300 text-sm font-semibold tracking-wide text-graphite-dark focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent transition-all uppercase placeholder:normal-case placeholder:font-normal placeholder:text-slate-400"
              disabled={loading}
              autoComplete="off"
              spellCheck="false"
            />
            {/* Mic Speech Button */}
            <button
              type="button"
              onClick={handleVoiceInput}
              disabled={loading}
              className={`absolute right-2.5 p-2 rounded-lg transition-colors ${
                isListening
                  ? 'bg-red-100 text-brand animate-pulse'
                  : 'text-slate-400 hover:text-brand hover:bg-slate-50'
              }`}
              title="Speak identifier / बोलकर बताएं"
            >
              {isListening ? <Mic className="w-5 h-5 text-brand" /> : <Mic className="w-5 h-5" />}
            </button>
          </div>
          {isListening && (
            <p className="text-xs text-brand font-medium mt-1.5 flex items-center space-x-1 animate-pulse">
              <span>●</span>
              <span>{t('entry.listening')}</span>
            </p>
          )}
        </div>

        {/* Suggestion Pill (Did you mean...?) */}
        {suggestion && (
          <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-900 flex items-start space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div className="flex-1">
              <span>{t('entry.didYouMean')}: </span>
              <button
                onClick={() => {
                  setInputVal(suggestion);
                  handleLookup(suggestion);
                }}
                className="font-bold underline text-brand hover:text-brand-dark ml-1"
              >
                {suggestion}
              </button>
              <p className="text-[11px] text-amber-700 mt-0.5">
                (Click to auto-correct and lookup)
              </p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {errorMsg && !suggestion && (
          <div className="p-3 bg-red-50 rounded-xl border border-red-200 text-xs text-red-800 flex items-start space-x-2">
            <AlertTriangle className="w-4 h-4 text-brand shrink-0 mt-0.5" />
            <span className="leading-snug">{errorMsg}</span>
          </div>
        )}

        {/* Primary CTA */}
        <button
          onClick={() => handleLookup()}
          disabled={loading || !inputVal.trim()}
          className="w-full py-3.5 px-4 rounded-xl bg-brand hover:bg-brand-dark text-white font-bold text-sm shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2"
        >
          {loading ? (
            <span className="inline-flex items-center space-x-2">
              <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
              <span>Verifying Registry...</span>
            </span>
          ) : (
            <>
              <span>{t('entry.cta')}</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>

        {/* No GST Alternative Path */}
        <div className="pt-2 border-t border-slate-100 text-center">
          <p className="text-xs text-graphite-light mb-2">{t('entry.noGstPrompt')}</p>
          <button
            onClick={handleNoGstPath}
            disabled={loading}
            className="text-xs font-bold text-brand hover:underline inline-flex items-center space-x-1"
          >
            <span>{t('entry.noGstAction')}</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>
      </div>

      {/* Trust Badges */}
      <div className="mt-8 grid grid-cols-3 gap-2 text-center text-[11px] text-graphite-light">
        <div className="p-2 bg-white/60 rounded-lg border border-slate-200/60">
          <span className="font-bold text-graphite-dark block">Zero Touch</span>
          <span>Auto-fetched</span>
        </div>
        <div className="p-2 bg-white/60 rounded-lg border border-slate-200/60">
          <span className="font-bold text-graphite-dark block">Deterministic</span>
          <span>No LLM hallucination</span>
        </div>
        <div className="p-2 bg-white/60 rounded-lg border border-slate-200/60">
          <span className="font-bold text-graphite-dark block">DPDP Ready</span>
          <span>Zero image storage</span>
        </div>
      </div>
    </div>
  );
};
