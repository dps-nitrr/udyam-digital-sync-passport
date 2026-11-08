import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { Search, Filter, UserCheck, Sparkles, AlertCircle, ArrowUpDown } from 'lucide-react';

const PARTNERS = [
  { id: 'P-DEL-01', name: 'Rajesh Verma (Delhi Field)' },
  { id: 'P-MUM-01', name: 'Priya Deshmukh (Mumbai Channel)' },
  { id: 'P-BLR-01', name: 'Karthik Rao (BLR Field)' },
  { id: 'P-HYD-01', name: 'Suresh Reddy (HYD Channel)' },
];

export const Leads: React.FC = () => {
  const [leads, setLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [segmentFilter, setSegmentFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [assignedMap, setAssignedMap] = useState<Record<string, string>>({});

  useEffect(() => {
    fetchLeads();
  }, [segmentFilter]);

  const fetchLeads = async () => {
    setLoading(true);
    try {
      const res = await api.getBackofficeLeads({
        segment: segmentFilter || undefined,
        outcome: 'Lost',
      });
      setLeads(res.leads);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAssign = async (leadId: string, partnerId: string) => {
    try {
      await api.assignPartner(leadId, partnerId);
      setAssignedMap((prev) => ({ ...prev, [leadId]: partnerId }));
    } catch (err: any) {
      alert(`Assignment failed: ${err.message}`);
    }
  };

  const filteredLeads = leads.filter((lead) => {
    if (priorityFilter && lead.priority_band !== priorityFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        lead.business_name?.toLowerCase().includes(q) ||
        lead.lead_id?.toLowerCase().includes(q) ||
        lead.city?.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="space-y-4">
      {/* Search & Filter Bar */}
      <div className="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-2xs flex flex-wrap gap-2 items-center justify-between text-xs">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search leads by business, ID, city..."
            className="w-full pl-9 pr-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-1 focus:ring-brand text-graphite-dark"
          />
        </div>

        <div className="flex items-center space-x-2">
          {/* Segment Filter */}
          <select
            value={segmentFilter}
            onChange={(e) => setSegmentFilter(e.target.value)}
            className="p-2 border border-slate-200 rounded-xl bg-slate-50 text-graphite-dark font-medium"
          >
            <option value="">All Segments</option>
            <option value="Micro retail & services">Micro retail & services</option>
            <option value="Professional offices">Professional offices</option>
            <option value="Small multi-site businesses">Small multi-site businesses</option>
            <option value="Small manufacturers">Small manufacturers</option>
          </select>

          {/* Priority Filter */}
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="p-2 border border-slate-200 rounded-xl bg-slate-50 text-graphite-dark font-medium"
          >
            <option value="">All Priorities</option>
            <option value="High">High Propensity (Top Decile)</option>
            <option value="Medium">Medium Propensity</option>
            <option value="Low">Low Propensity</option>
          </select>
        </div>
      </div>

      {/* Leads Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden text-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900 text-white text-[11px] font-bold uppercase tracking-wider">
                <th className="p-3">Lead ID</th>
                <th className="p-3">Business / City</th>
                <th className="p-3">Segment</th>
                <th className="p-3">Drop Reason</th>
                <th className="p-3">Propensity Score</th>
                <th className="p-3">Recommended Action</th>
                <th className="p-3">Assign Partner</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-graphite-dark">
              {loading ? (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-slate-400 font-semibold">
                    Loading ML propensity rankings...
                  </td>
                </tr>
              ) : filteredLeads.length === 0 ? (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-slate-400 font-semibold">
                    No matching unclosed leads found.
                  </td>
                </tr>
              ) : (
                filteredLeads.slice(0, 30).map((l) => {
                  const assigned = assignedMap[l.lead_id] || l.assigned_partner;
                  const isHigh = l.priority_band === 'High';
                  const isMed = l.priority_band === 'Medium';
                  return (
                    <tr key={l.lead_id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="p-3 font-mono text-[11px] font-bold text-slate-500">
                        {l.lead_id}
                      </td>
                      <td className="p-3 font-semibold">
                        <span className="block text-graphite-dark font-bold">
                          {l.business_name}
                        </span>
                        <span className="text-[10px] text-slate-400">
                          {l.city}, {l.state}
                        </span>
                      </td>
                      <td className="p-3 text-[11px] text-slate-600 font-medium">
                        {l.segment}
                      </td>
                      <td className="p-3 text-[11px] text-rose-800 font-medium">
                        {l.drop_reason || 'Needs Assessment'}
                      </td>
                      <td className="p-3">
                        <div className="flex items-center space-x-1.5">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider ${
                              isHigh
                                ? 'bg-green-100 text-success border border-green-300'
                                : isMed
                                ? 'bg-amber-100 text-warn border border-amber-300'
                                : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            {(l.propensity_score * 100).toFixed(0)}% • {l.priority_band}
                          </span>
                        </div>
                      </td>
                      <td className="p-3 text-[11px] text-slate-600 leading-snug">
                        {l.recommended_action}
                      </td>
                      <td className="p-3">
                        <select
                          value={assigned || ''}
                          onChange={(e) => handleAssign(l.lead_id, e.target.value)}
                          className="p-1 border border-slate-200 rounded text-[11px] bg-slate-50 text-graphite-dark font-medium"
                        >
                          <option value="">Unassigned</option>
                          {PARTNERS.map((p) => (
                            <option key={p.id} value={p.id}>
                              {p.name}
                            </option>
                          ))}
                        </select>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
