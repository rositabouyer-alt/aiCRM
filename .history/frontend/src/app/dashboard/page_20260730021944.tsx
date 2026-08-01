"use client";
import { useEffect, useState } from "react";
import { Users, MessageSquare, CalendarCheck, TrendingUp, Bot, Send, Phone, ArrowUpRight } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";

const chartData = [
  { name: "Mon", leads: 12, bookings: 5 },
  { name: "Tue", leads: 19, bookings: 8 },
  { name: "Wed", leads: 15, bookings: 6 },
  { name: "Thu", leads: 27, bookings: 11 },
  { name: "Fri", leads: 22, bookings: 9 },
  { name: "Sat", leads: 30, bookings: 14 },
  { name: "Sun", leads: 18, bookings: 7 },
];

const sourceData = [
  { name: "Telegram", value: 45 },
  { name: "Website", value: 30 },
  { name: "Direct", value: 15 },
  { name: "Other", value: 10 },
];

const statusColors: Record<string, string> = {
  new: "badge-new",
  active: "badge-active",
  qualified: "badge-qualified",
  booked: "badge-booked",
  closed: "badge-closed",
};

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="glass-card px-3 py-2 text-xs border border-pink-500/20">
        <p className="text-slate-400 mb-1">{label}</p>
        {payload.map((p: any) => (
          <p key={p.name} style={{ color: p.color }} className="font-medium">{p.name}: {p.value}</p>
        ))}
      </div>
    );
  }
  return null;
};

export default function DashboardPage() {
  const [stats, setStats] = useState({
    total_leads: 0,
    active_conversations: 0,
    total_bookings: 0,
    conversion_rate: 0,
  });
  const [recentLeads, setRecentLeads] = useState<any[]>([]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const analyticsRes = await fetch("http://localhost:8000/api/analytics/summary");
      if (analyticsRes.ok) {
        const data = await analyticsRes.json();
        setStats(data);
      }

      const leadsRes = await fetch("http://localhost:8000/api/leads/?limit=5");
      if (leadsRes.ok) {
        const data = await leadsRes.json();
        setRecentLeads(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      console.error("Error fetching data:", err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-white">Dashboard</h1>
          <p className="text-slate-600 text-sm mt-0.5">Welcome back — here's what's happening</p>
        </div>
        <div className="flex items-center gap-2 glass-card px-3 py-2 border-pink-500/20">
          <Bot className="w-4 h-4 text-accent" />
          <span className="text-xs text-slate-300">AI handled <span className="text-white font-medium">89%</span> today</span>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="glass-card p-5">
          <div className="flex items-start justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-pink-500/10 border border-pink-500/20 flex items-center justify-center">
              <Users className="w-5 h-5 text-pink-400" />
            </div>
            <span className="text-xs text-emerald-400 font-medium flex items-center gap-0.5">
              <ArrowUpRight className="w-3 h-3" />+12%
            </span>
          </div>
          <p className="text-2xl font-semibold text-white">{stats.total_leads}</p>
          <p className="text-slate-600 text-xs mt-1">Total Leads</p>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-start justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-violet-400" />
            </div>
            <span className="text-xs text-emerald-400 font-medium flex items-center gap-0.5">
              <ArrowUpRight className="w-3 h-3" />+8%
            </span>
          </div>
          <p className="text-2xl font-semibold text-white">{stats.active_conversations}</p>
          <p className="text-slate-600 text-xs mt-1">Active Conversations</p>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-start justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
              <CalendarCheck className="w-5 h-5 text-emerald-400" />
            </div>
            <span className="text-xs text-emerald-400 font-medium flex items-center gap-0.5">
              <ArrowUpRight className="w-3 h-3" />+23%
            </span>
          </div>
          <p className="text-2xl font-semibold text-white">{stats.total_bookings}</p>
          <p className="text-slate-600 text-xs mt-1">Bookings This Month</p>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-start justify-between mb-4">
            <div className="w-10 h-10 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-yellow-400" />
            </div>
            <span className="text-xs text-emerald-400 font-medium flex items-center gap-0.5">
              <ArrowUpRight className="w-3 h-3" />+4%
            </span>
          </div>
          <p className="text-2xl font-semibold text-white">{stats.conversion_rate?.toFixed(1) || 0}%</p>
          <p className="text-slate-600 text-xs mt-1">Conversion Rate</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2 glass-card p-5">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-sm font-medium text-white">Leads & Bookings</h2>
            <span className="text-xs text-slate-600">Last 7 days</span>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="leads" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ff2d78" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#ff2d78" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="bookings" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#bf5af2" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#bf5af2" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,45,120,0.06)" />
              <XAxis dataKey="name" tick={{ fill: "#4b5563", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#4b5563", fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="leads" stroke="#ff2d78" strokeWidth={2} fill="url(#leads)" />
              <Area type="monotone" dataKey="bookings" stroke="#bf5af2" strokeWidth={2} fill="url(#bookings)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-sm font-medium text-white">Lead Sources</h2>
            <span className="text-xs text-slate-600">This month</span>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={sourceData} layout="vertical">
              <XAxis type="number" tick={{ fill: "#4b5563", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis dataKey="name" type="category" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} width={55} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" fill="#ff2d78" radius={[0, 4, 4, 0]} fillOpacity={0.85} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-card">
        <div className="flex items-center justify-between p-5 border-b border-pink-500/10">
          <h2 className="text-sm font-medium text-white">Recent Leads</h2>
          <button className="text-xs text-accent hover:text-accent-light transition-colors">View all</button>
        </div>
        <div className="divide-y divide-pink-500/[0.06]">
          {recentLeads.length === 0 ? (
            <div className="p-5 text-center text-slate-600 text-sm">هنوز لیدی وجود ندارد</div>
          ) : (
            recentLeads.map((lead, i) => (
              <div key={i} className="flex items-center gap-4 px-5 py-3.5 hover:bg-white/[0.02] transition-colors">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-accent/40 to-violet-500/40 border border-accent/20 flex items-center justify-center text-white text-xs font-medium shrink-0">
                  {lead.full_name?.[0] || "?"}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-white text-sm font-medium truncate">{lead.full_name || "بدون نام"}</p>
                  <p className="text-slate-600 text-xs">{lead.platform || "website"}</p>
                </div>
                <span className="text-slate-500 text-xs font-medium">${lead.budget || "0"}</span>
                <span className="badge-new">{lead.status || "new"}</span>
                <div className="flex gap-1.5">
                  <button className="w-7 h-7 rounded-lg bg-white/[0.03] hover:bg-accent/20 flex items-center justify-center">
                    <MessageSquare className="w-3.5 h-3.5 text-slate-600" />
                  </button>
                  <button className="w-7 h-7 rounded-lg bg-white/[0.03] hover:bg-emerald-500/20 flex items-center justify-center">
                    <Phone className="w-3.5 h-3.5 text-slate-600" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="glass-card p-5">
        <div className="flex items-center gap-2 mb-4">
          <Bot className="w-4 h-4 text-accent" />
          <h2 className="text-sm font-medium text-white">AI Activity</h2>
          <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
        </div>
        <div className="space-y-2.5">
          {[
            { msg: "Processing new conversations", time: "just now" },
            { msg: "Qualified leads automatically", time: "5m ago" },
            { msg: "Sent follow-up messages", time: "1h ago" },
            { msg: "Creating booking tasks", time: "2h ago" },
          ].map((item, i) => (
            <div key={i} className="flex items-start gap-3 text-xs">
              <div className="w-1.5 h-1.5 rounded-full bg-pink-400 mt-1.5" />
              <span className="text-slate-400 flex-1">{item.msg}</span>
              <span className="text-slate-700">{item.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
