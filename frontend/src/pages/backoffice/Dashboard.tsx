import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
} from 'recharts';
import { TrendingUp, Users, Clock, ShieldCheck, CheckCircle2, AlertOctagon } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const res = await api.getFunnelMetrics();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-xs text-graphite-light">
        Loading funnel metrics...
      </div>
    );
  }

  // Fallback demo metrics if API is connecting
  const funnelData = data?.funnel || [
    { stage: 'Contacted', count: 5000, drop_rate: 0 },
    { stage: 'Needs Assessed', count: 3200, drop_rate: 36 },
    { stage: 'Quote Accepted', count: 1450, drop_rate: 54 },
    { stage: 'KYC Submitted', count: 720, drop_rate: 50 },
    { stage: 'Activated', count: 368, drop_rate: 49 },
  ];

  const dropReasons = data?.drop_reasons || [
    { reason: 'Price too high / opaque', count: 820, fixable: true },
    { reason: 'KYC doc friction / delay', count: 640, fixable: true },
    { reason: 'Competitor fiber chosen', count: 580, fixable: false },
    { reason: 'Wrong product proposed', count: 420, fixable: true },
    { reason: 'Coverage not available', count: 350, fixable: false },
  ];

  return (
    <div className="space-y-4">
      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-[11px] font-bold uppercase tracking-wider">
              Total SMB Leads
            </span>
            <Users className="w-4 h-4 text-brand" />
          </div>
          <span className="text-2xl font-black text-graphite-dark block">
            5,000
          </span>
          <span className="text-[10px] text-graphite-light block">
            Historical Baseline
          </span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-[11px] font-bold uppercase tracking-wider">
              Baseline Conversion
            </span>
            <TrendingUp className="w-4 h-4 text-amber-500" />
          </div>
          <span className="text-2xl font-black text-graphite-dark block">
            7.36%
          </span>
          <span className="text-[10px] text-green-600 font-bold block">
            +1.90x Lift in Top Decile
          </span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-[11px] font-bold uppercase tracking-wider">
              Digital-Fixable Drops
            </span>
            <ShieldCheck className="w-4 h-4 text-success" />
          </div>
          <span className="text-2xl font-black text-brand block">
            58.4%
          </span>
          <span className="text-[10px] text-graphite-light block">
            Solvable by Sync Passport
          </span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-[11px] font-bold uppercase tracking-wider">
              Cycle Time to Active
            </span>
            <Clock className="w-4 h-4 text-cyan-600" />
          </div>
          <span className="text-2xl font-black text-graphite-dark block">
            3.2 Days
          </span>
          <span className="text-[10px] text-green-600 font-bold block">
            Down from 18.4 Days
          </span>
        </div>
      </div>

      {/* Funnel & Drop Reason Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Funnel Conversion Bar Chart */}
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-extrabold text-xs text-graphite-dark uppercase tracking-wider">
              SMB Onboarding Funnel
            </h3>
            <span className="text-[10px] font-semibold text-slate-400">
              Drop-off per milestone
            </span>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                <XAxis
                  dataKey="stage"
                  tick={{ fontSize: 10, fill: '#64748B' }}
                  angle={-15}
                  textAnchor="end"
                />
                <YAxis tick={{ fontSize: 10, fill: '#64748B' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0F172A',
                    borderRadius: '8px',
                    color: '#FFF',
                    fontSize: '11px',
                  }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {funnelData.map((entry: any, index: number) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={index === funnelData.length - 1 ? '#15803D' : '#B91C1C'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Drop Reasons Analysis */}
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-extrabold text-xs text-graphite-dark uppercase tracking-wider">
              Why Unclosed Leads Dropped
            </h3>
            <span className="text-[10px] font-semibold text-brand">
              Green = Fixed by Sync Passport
            </span>
          </div>

          <div className="space-y-2 pt-1 text-xs">
            {dropReasons.map((dr: any, idx: number) => (
              <div
                key={idx}
                className="p-2.5 rounded-xl border border-slate-100 flex items-center justify-between bg-slate-50/60"
              >
                <div className="flex items-center space-x-2">
                  <div
                    className={`w-2.5 h-2.5 rounded-full ${
                      dr.fixable ? 'bg-success' : 'bg-slate-300'
                    }`}
                  />
                  <div>
                    <span className="font-bold text-graphite-dark block text-[11px]">
                      {dr.reason}
                    </span>
                    <span className="text-[10px] text-slate-400">
                      {dr.fixable ? 'Automated by GST-first engine' : 'Macro / Network constraint'}
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="font-extrabold text-graphite-dark text-xs block">
                    {dr.count} leads
                  </span>
                  <span
                    className={`text-[9px] font-bold uppercase tracking-wider ${
                      dr.fixable ? 'text-success font-black' : 'text-slate-400'
                    }`}
                  >
                    {dr.fixable ? 'DIGITAL FIXABLE' : 'INFRA'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
