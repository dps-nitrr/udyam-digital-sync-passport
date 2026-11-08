import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useJourneyStore } from '../store/journey';
import { api } from '../api/client';
import confetti from 'canvas-confetti';
import {
  CheckCircle2,
  Clock,
  Calendar,
  MessageSquare,
  Sparkles,
  Zap,
  ShieldCheck,
  Smartphone,
  Send,
  AlertCircle,
} from 'lucide-react';

const STAGE_ORDER = [
  'quote_accepted',
  'kyc_approved',
  'order_booked',
  'feasibility_passed',
  'installed',
  'activated',
];

export const Tracker: React.FC = () => {
  const { t } = useTranslation();
  const { order, setOrder, journeyId } = useJourneyStore();

  const [loading, setLoading] = useState(false);
  const [showOtpModal, setShowOtpModal] = useState(false);
  const [otpInput, setOtpInput] = useState('');
  const [otpError, setOtpError] = useState<string | null>(null);

  // Normalize order fields across snake_case and camelCase
  const orderId = (order as any)?.order_id || (order as any)?.orderId || '';
  const promisedDate = (order as any)?.promised_date || (order as any)?.promisedDate || '2026-07-24';
  const currentStatus = (order as any)?.status || (order as any)?.current_status || (order as any)?.currentStatus || 'quote_accepted';
  const notifications = (order as any)?.notifications || [];

  useEffect(() => {
    // If order is activated, trigger confetti
    if (currentStatus === 'activated') {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.5 },
      });
    }
  }, [currentStatus]);

  if (!order) {
    return (
      <div className="w-full max-w-mobile mx-auto px-4 py-8 text-center text-xs text-graphite-light">
        <p>No active order found.</p>
      </div>
    );
  }

  const currentIdx = STAGE_ORDER.indexOf(currentStatus) >= 0 ? STAGE_ORDER.indexOf(currentStatus) : 0;

  const handleAdvanceDay = async () => {
    if (!orderId) return;
    setLoading(true);
    try {
      const res = await api.simulateAdvanceOrder(orderId, 1);
      setOrder(res);
      const newStatus = (res as any).status || (res as any).current_status;
      if (newStatus === 'activated') {
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.5 } });
      }
    } catch (err: any) {
      alert(`Advance failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    setLoading(true);
    setOtpError(null);
    try {
      await api.verifyOtp(otpInput);
      // Advance to activated
      if (orderId) {
        const res = await api.simulateAdvanceOrder(orderId, 5);
        setOrder(res);
      }
      setShowOtpModal(false);
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.5 },
      });
    } catch (err: any) {
      setOtpError(err.message || 'Invalid code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-mobile mx-auto px-4 py-5 space-y-4">
      {/* Title */}
      <div className="text-center space-y-1">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-green-50 border border-green-200 text-success text-xs font-semibold mb-1">
          <Zap className="w-3.5 h-3.5" />
          <span>Real-Time Provisioning</span>
        </div>
        <h2 className="text-xl font-black text-graphite-dark tracking-tight">
          {t('tracker.title')}
        </h2>
        <p className="text-xs text-graphite-light font-mono">
          {t('tracker.orderId')}: {orderId ? `#${orderId.slice(0, 8).toUpperCase()}` : '#ORD-DEMO-01'}
        </p>
      </div>

      {/* SLA & Promised Date Banner */}
      <div className="bg-slate-900 text-white rounded-2xl p-4 shadow-md space-y-2 border border-slate-700">
        <div className="flex items-center justify-between text-xs">
          <span className="font-extrabold text-amber-400 uppercase tracking-wider text-[10px] flex items-center space-x-1">
            <Calendar className="w-3.5 h-3.5" />
            <span>Guaranteed Activation SLA</span>
          </span>
          <span className="text-slate-300 font-bold">{promisedDate}</span>
        </div>
        <p className="text-[11px] text-slate-300 leading-relaxed">
          {t('tracker.delayGuarantee')}
        </p>
      </div>

      {/* 6-Stage Visual Timeline */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 text-xs space-y-3">
        <span className="font-extrabold text-graphite-dark block uppercase tracking-wider text-[11px]">
          Fulfillment Milestone Chain
        </span>
        <div className="relative pl-6 space-y-4">
          {/* Vertical Connecting Line */}
          <div className="absolute left-2.5 top-2 bottom-2 w-0.5 bg-slate-200 -translate-x-1/2" />

          {STAGE_ORDER.map((stageKey, idx) => {
            const isCompleted = idx <= currentIdx;
            const isCurrent = idx === currentIdx;
            return (
              <div key={stageKey} className="relative flex items-start space-x-3">
                {/* Stage Indicator Dot */}
                <div
                  className={`absolute -left-6 w-5 h-5 rounded-full flex items-center justify-center text-white text-[10px] font-bold shadow-xs transition-all ${
                    isCompleted
                      ? 'bg-success ring-4 ring-green-100'
                      : 'bg-slate-200 text-slate-500'
                  }`}
                >
                  {isCompleted ? '✓' : idx + 1}
                </div>

                <div className="space-y-0.5">
                  <span
                    className={`font-bold block ${
                      isCurrent
                        ? 'text-brand font-black'
                        : isCompleted
                        ? 'text-graphite-dark'
                        : 'text-slate-400'
                    }`}
                  >
                    {t(`tracker.stages.${stageKey}`)}
                  </span>
                  {isCurrent && (
                    <span className="text-[10px] text-brand font-semibold block animate-pulse">
                      ● Active In Progress
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* WhatsApp Simulated Phone Feed */}
      <div className="bg-[#E5DDD5] rounded-3xl p-3 shadow-md border-4 border-slate-800 space-y-2">
        {/* WhatsApp Header */}
        <div className="bg-[#075E54] text-white px-3 py-2 rounded-2xl flex items-center space-x-2 shadow-xs">
          <div className="w-7 h-7 rounded-full bg-white flex items-center justify-center text-[#075E54] font-bold text-xs">
            AB
          </div>
          <div>
            <span className="font-bold text-xs block leading-tight">
              Accel Business Verified
            </span>
            <span className="text-[9px] text-green-200 block">
              Official WhatsApp Notification Bot
            </span>
          </div>
        </div>

        {/* WhatsApp Chat Bubbles */}
        <div className="space-y-2 max-h-52 overflow-y-auto p-1">
          {notifications && notifications.length > 0 ? (
            notifications.map((notif: any, i: number) => (
              <div
                key={i}
                className="bg-white rounded-xl rounded-tl-none p-2.5 max-w-[88%] text-[11px] text-slate-800 shadow-2xs space-y-1"
              >
                <p className="leading-snug">{notif.body}</p>
                <span className="text-[9px] text-slate-400 block text-right">
                  {(notif.ts || notif.timestamp)?.slice(11, 16) || 'Just now'} ✓✓
                </span>
              </div>
            ))
          ) : (
            <div className="bg-white rounded-xl p-2.5 text-[11px] text-slate-500 text-center">
              Welcome to Accel Business! Your order updates will stream here.
            </div>
          )}
        </div>
      </div>

      {/* Demo Controls */}
      <div className="grid grid-cols-2 gap-2 pt-1">
        <button
          onClick={handleAdvanceDay}
          disabled={loading || currentStatus === 'activated'}
          className="py-3 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-sm flex items-center justify-center space-x-1.5 transition-all"
        >
          <Clock className="w-3.5 h-3.5 text-amber-400" />
          <span>{t('tracker.btnAdvance')}</span>
        </button>

        <button
          onClick={() => setShowOtpModal(true)}
          disabled={loading || currentStatus === 'activated'}
          className="py-3 px-3 rounded-xl bg-brand hover:bg-brand-dark text-white font-bold text-xs shadow-sm flex items-center justify-center space-x-1.5 transition-all"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Simulate OTP</span>
        </button>
      </div>

      {/* Demo OTP Modal */}
      {showOtpModal && (
        <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-xs w-full p-5 space-y-3 text-xs shadow-xl text-center">
            <h3 className="font-black text-sm text-graphite-dark">
              {t('tracker.otpModalTitle')}
            </h3>
            <p className="text-graphite-light text-xs">
              {t('tracker.otpPrompt')}
            </p>
            <input
              type="text"
              maxLength={6}
              value={otpInput}
              onChange={(e) => setOtpInput(e.target.value)}
              placeholder="123456"
              className="w-full text-center tracking-widest text-lg font-black py-2.5 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand"
            />
            {otpError && (
              <p className="text-[11px] text-danger font-semibold">{otpError}</p>
            )}
            <button
              onClick={handleVerifyOtp}
              disabled={loading || otpInput.length < 6}
              className="w-full py-2.5 bg-brand text-white font-bold rounded-xl shadow-md"
            >
              {t('tracker.btnVerifyOtp')}
            </button>
            <button
              onClick={() => setShowOtpModal(false)}
              className="w-full py-1 text-slate-400 font-semibold"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
