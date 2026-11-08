import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { api } from '../api/client';
import {
  Check,
  ChevronDown,
  ChevronUp,
  Plus,
  Minus,
  Info,
  Calendar,
  ShieldAlert,
  ArrowRight,
  TrendingDown,
  Tag,
  Sparkles,
} from 'lucide-react';

export const Quote: React.FC = () => {
  const { t } = useTranslation();
  const { journeyId, quote, quoteExplanation, setQuote, setStep } = useJourneyStore();

  const [loading, setLoading] = useState(false);
  const [expandedWhy, setExpandedWhy] = useState<Record<string, boolean>>({});
  const [showExcluded, setShowExcluded] = useState(false);
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  if (!quote) {
    return (
      <div className="w-full max-w-mobile mx-auto px-4 py-8 text-center">
        <p className="text-xs text-graphite-light">No active quote found.</p>
        <button
          onClick={() => setStep('ENTRY')}
          className="mt-4 px-4 py-2 bg-brand text-white rounded-lg text-xs font-bold"
        >
          Start New Journey
        </button>
      </div>
    );
  }

  const showToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(null), 4000);
  };

  // Switch contract term (12 vs 24 months) — Calls backend!
  const handleTermChange = async (newTerm: number) => {
    if (!journeyId || newTerm === quote.term_months) return;
    setLoading(true);
    try {
      const res = await api.updateQuote(journeyId, newTerm);
      setQuote(res.quote as any);
      showToast(`Updated to ${newTerm}-month contract term pricing.`);
    } catch (err: any) {
      alert(`Update failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Change quantity stepper — Calls backend!
  const handleQtyChange = async (productId: string, currentQty: number, delta: number) => {
    if (!journeyId) return;
    const newQty = Math.max(1, currentQty + delta);
    if (newQty === currentQty) return;

    setLoading(true);
    try {
      const res = await api.updateQuote(journeyId, undefined, { [productId]: newQty });
      setQuote(res.quote as any);
    } catch (err: any) {
      alert(`Quantity update failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Toggle Add-on — Calls backend!
  const handleToggleProduct = async (productId: string, currentState: boolean) => {
    if (!journeyId) return;
    setLoading(true);
    try {
      const res = await api.updateQuote(journeyId, undefined, undefined, {
        [productId]: !currentState,
      });
      setQuote(res.quote as any);
      if (res.auto_added.length > 0) {
        showToast(`Auto-added required dependency: ${res.auto_added.join(', ')}`);
      }
    } catch (err: any) {
      alert(`Toggle failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptQuote = async () => {
    if (!journeyId) return;
    setLoading(true);
    try {
      await api.acceptQuote(journeyId);
      setStep('CONSENT');
    } catch (err: any) {
      alert(`Failed to accept quote: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const activeBundleItems = quote.bundle.filter((b) => b.active);
  const inactiveBundleItems = quote.bundle.filter((b) => !b.active);

  return (
    <div className="w-full max-w-mobile mx-auto px-4 py-5 space-y-4">
      {/* Toast Alert */}
      {toastMsg && (
        <div className="fixed top-16 left-1/2 -translate-x-1/2 z-50 px-4 py-2 bg-slate-900 text-white text-xs font-semibold rounded-full shadow-lg flex items-center space-x-1.5 border border-slate-700 animate-fade-in">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span>{toastMsg}</span>
        </div>
      )}

      {/* Hero Monthly Price Card */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white rounded-3xl p-5 shadow-lg border border-slate-700 space-y-3 relative overflow-hidden">
        <div className="flex items-center justify-between text-xs">
          <span className="font-extrabold text-amber-400 tracking-wider uppercase text-[10px] flex items-center space-x-1">
            <Tag className="w-3 h-3" />
            <span>Guaranteed Fixed Price</span>
          </span>
          <span className="text-[11px] font-semibold text-slate-300">
            {quote.bundle.length} Solutions Unified
          </span>
        </div>

        {/* Hero Price */}
        <div>
          <div className="flex items-baseline space-x-1">
            <span className="text-3xl font-black tracking-tight text-white">
              ₹{quote.monthly_recurring.toLocaleString('en-IN')}
            </span>
            <span className="text-slate-300 text-sm font-semibold">
              {t('quote.perMonth')}
            </span>
          </div>
          <span className="text-xs text-slate-400 font-medium block mt-0.5">
            {t('quote.plusGst')} (Transparent monthly billing)
          </span>
        </div>

        {/* Current Spend Savings Comparison */}
        {quote.vs_current_spend && quote.vs_current_spend < 0 && (
          <div className="px-3 py-1.5 bg-green-950/70 border border-green-500/40 rounded-xl text-green-300 text-xs font-semibold flex items-center space-x-1.5">
            <TrendingDown className="w-4 h-4 text-green-400 shrink-0" />
            <span>
              {t('quote.savingNotice', {
                amount: Math.abs(Math.round(quote.vs_current_spend)).toLocaleString('en-IN'),
              })}
            </span>
          </div>
        )}

        {/* Contract Term Selector Toggle (Calls backend to recalculate) */}
        <div className="pt-2 border-t border-slate-700/80">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
            {t('quote.contractTerm')}
          </span>
          <div className="grid grid-cols-2 gap-2 bg-slate-950/60 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => handleTermChange(12)}
              disabled={loading}
              className={`py-1.5 px-3 rounded-lg text-xs font-bold transition-all ${
                quote.term_months === 12
                  ? 'bg-brand text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              12 Months
            </button>
            <button
              onClick={() => handleTermChange(24)}
              disabled={loading}
              className={`py-1.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center space-x-1 ${
                quote.term_months === 24
                  ? 'bg-brand text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <span>24 Months</span>
              <span className="text-[9px] px-1 py-0.2 rounded bg-amber-400 text-slate-950 font-extrabold">
                SAVE 15%
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* Guaranteed Promised Date Pill */}
      <div className="px-4 py-2.5 bg-white rounded-xl border border-slate-200 shadow-sm flex items-center justify-between text-xs">
        <div className="flex items-center space-x-2 text-graphite-dark">
          <Calendar className="w-4 h-4 text-brand" />
          <span className="font-semibold">{t('quote.promisedInstall')}:</span>
        </div>
        <span className="font-black text-brand bg-red-50 px-2 py-0.5 rounded border border-red-100">
          {quote.promised_date}
        </span>
      </div>

      {/* Core Bundle List */}
      <div className="space-y-2">
        <div className="flex items-center justify-between px-1">
          <span className="text-xs font-black text-graphite-dark uppercase tracking-wider">
            {t('quote.bundleItems')}
          </span>
          <span className="text-[11px] text-graphite-light">
            All prices deterministically locked
          </span>
        </div>

        <div className="space-y-2">
          {activeBundleItems.map((item) => {
            const isWhyOpen = !!expandedWhy[item.product_id];
            return (
              <div
                key={item.product_id}
                className="bg-white rounded-2xl border border-slate-200 shadow-sm p-3.5 space-y-2 text-xs transition-all"
              >
                <div className="flex items-start justify-between">
                  <div className="space-y-0.5 flex-1 pr-2">
                    <div className="flex items-center space-x-1.5">
                      <span className="font-bold text-graphite-dark text-sm">
                        {item.name_plain}
                      </span>
                      <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-100 text-graphite-light font-mono">
                        {item.product_id}
                      </span>
                    </div>
                    <span className="text-[11px] text-graphite-light block">
                      {item.category} • ₹{item.unit_price} / {item.unit}
                    </span>
                  </div>

                  {/* Quantity Stepper */}
                  <div className="flex items-center space-x-1.5 bg-slate-50 border border-slate-200 rounded-lg p-1">
                    <button
                      onClick={() => handleQtyChange(item.product_id, item.qty, -1)}
                      disabled={loading || item.qty <= 1}
                      className="p-1 rounded bg-white text-slate-700 hover:text-brand disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
                    >
                      <Minus className="w-3 h-3" />
                    </button>
                    <span className="w-6 text-center font-bold text-graphite-dark text-xs">
                      {item.qty}
                    </span>
                    <button
                      onClick={() => handleQtyChange(item.product_id, item.qty, 1)}
                      disabled={loading}
                      className="p-1 rounded bg-white text-slate-700 hover:text-brand disabled:opacity-40 shadow-2xs"
                    >
                      <Plus className="w-3 h-3" />
                    </button>
                  </div>
                </div>

                {/* Line Price & Why Expander */}
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                  <button
                    onClick={() =>
                      setExpandedWhy((prev) => ({
                        ...prev,
                        [item.product_id]: !prev[item.product_id],
                      }))
                    }
                    className="text-[11px] font-semibold text-brand hover:underline flex items-center space-x-1"
                  >
                    <Info className="w-3 h-3" />
                    <span>{t('quote.whyIncluded')}</span>
                    {isWhyOpen ? (
                      <ChevronUp className="w-3 h-3" />
                    ) : (
                      <ChevronDown className="w-3 h-3" />
                    )}
                  </button>

                  <div className="text-right">
                    <span className="font-extrabold text-sm text-graphite-dark">
                      ₹{item.line_total.toLocaleString('en-IN')}
                    </span>
                    <span className="text-[10px] text-graphite-light block">/ month</span>
                  </div>
                </div>

                {/* Why Dropdown */}
                {isWhyOpen && (
                  <div className="p-2.5 bg-red-50/60 rounded-xl border border-red-100 text-[11px] text-graphite-dark leading-relaxed animate-fade-in">
                    {item.why}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Optional Add-Ons Toggle List */}
      {inactiveBundleItems.length > 0 && (
        <div className="space-y-2 pt-2">
          <span className="text-xs font-black text-graphite-dark uppercase tracking-wider block px-1">
            {t('quote.addOns')}
          </span>
          <div className="space-y-2">
            {inactiveBundleItems.map((addon) => (
              <div
                key={addon.product_id}
                className="bg-white rounded-xl border border-slate-200 p-3 flex items-center justify-between text-xs"
              >
                <div className="space-y-0.5">
                  <div className="flex items-center space-x-1.5">
                    <span className="font-bold text-graphite-dark">{addon.name_plain}</span>
                    <span className="text-[10px] text-graphite-light">({addon.product_id})</span>
                  </div>
                  <span className="text-[11px] text-graphite-light block">
                    +₹{addon.unit_price} / month • {addon.why}
                  </span>
                </div>
                <button
                  onClick={() => handleToggleProduct(addon.product_id, false)}
                  disabled={loading}
                  className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-brand hover:text-white text-graphite-dark font-bold text-xs border border-slate-200 transition-colors"
                >
                  + Add
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* First Invoice Breakdown */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 space-y-2 text-xs">
        <span className="font-extrabold text-graphite-dark block text-xs border-b border-slate-100 pb-2">
          {t('quote.firstInvoice')}
        </span>
        <div className="flex items-center justify-between text-graphite-light">
          <span>{t('quote.monthlyRecurring')}</span>
          <span className="font-semibold text-graphite-dark">
            ₹{quote.monthly_recurring.toLocaleString('en-IN')}
          </span>
        </div>
        <div className="flex items-center justify-between text-graphite-light">
          <span>{t('quote.setupFee')}</span>
          <span className="font-semibold text-graphite-dark">
            ₹{quote.one_time_setup.toLocaleString('en-IN')}
          </span>
        </div>
        <div className="flex items-center justify-between text-graphite-light">
          <span>{t('quote.gstTax')}</span>
          <span className="font-semibold text-graphite-dark">
            ₹{quote.gst_amount.toLocaleString('en-IN')}
          </span>
        </div>
        <div className="pt-2 border-t border-slate-200 flex items-center justify-between font-black text-sm text-graphite-dark">
          <span>{t('quote.firstInvoiceTotal')}</span>
          <span className="text-base text-brand">
            ₹{quote.first_invoice.toLocaleString('en-IN')}
          </span>
        </div>
      </div>

      {/* Collapsible Excluded Products */}
      {quote.excluded && quote.excluded.length > 0 && (
        <div className="bg-slate-50 rounded-xl border border-slate-200 p-3 text-xs">
          <button
            onClick={() => setShowExcluded(!showExcluded)}
            className="w-full flex items-center justify-between font-bold text-graphite-light"
          >
            <span>
              {t('quote.excludedTitle')} ({quote.excluded.length})
            </span>
            {showExcluded ? (
              <ChevronUp className="w-3.5 h-3.5" />
            ) : (
              <ChevronDown className="w-3.5 h-3.5" />
            )}
          </button>
          {showExcluded && (
            <div className="mt-3 space-y-2 border-t border-slate-200 pt-2">
              {quote.excluded.map((ex) => (
                <div key={ex.product_id} className="flex items-start justify-between text-[11px]">
                  <span className="font-semibold text-graphite-dark">{ex.product_name}</span>
                  <span className="text-slate-500 italic text-right pl-2">
                    {ex.reason_plain}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Accept Quote CTA Button */}
      <button
        onClick={handleAcceptQuote}
        disabled={loading}
        className="w-full py-4 px-4 rounded-xl bg-brand hover:bg-brand-dark text-white font-extrabold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center space-x-2"
      >
        <span>{t('quote.btnAccept')}</span>
        <ArrowRight className="w-4 h-4" />
      </button>
    </div>
  );
};
