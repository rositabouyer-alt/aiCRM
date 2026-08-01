"use client";
import { Download, FileJson, Package } from "lucide-react";
import { useState } from "react";

export default function DownloadsPage() {
  const [loading, setLoading] = useState(false);

  const handleDownload = async (endpoint: string, filename: string) => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api${endpoint}`);
      const data = await res.json();
      
      const element = document.createElement("a");
      element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2)));
      element.setAttribute("download", filename);
      element.style.display = "none";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      alert("✅ دانلود شد!");
    } catch (err) {
      alert("❌ خطا در دانلود!");
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <h1 className="text-xl font-semibold text-white flex items-center gap-2">
        <Download className="w-5 h-5 text-accent" />
        Downloads
      </h1>

      <div className="grid grid-cols-2 gap-4">
        <div className="glass-card p-6 hover:bg-white/[0.06] cursor-pointer transition-all">
          <FileJson className="w-8 h-8 text-accent mb-3" />
          <h3 className="text-white font-medium mb-2">Leads</h3>
          <p className="text-slate-600 text-sm mb-4">تمام لیدها به صورت JSON</p>
          <button 
            onClick={() => handleDownload("/exports/leads/json", "leads.json")}
            disabled={loading}
            className="bg-accent hover:bg-accent-hover text-white font-medium px-4 py-2 rounded-xl transition-all text-sm disabled:opacity-50"
          >
            {loading ? "درحال دانلود..." : "دانلود"}
          </button>
        </div>

        <div className="glass-card p-6 hover:bg-white/[0.06] cursor-pointer transition-all">
          <Package className="w-8 h-8 text-violet-400 mb-3" />
          <h3 className="text-white font-medium mb-2">Conversations</h3>
          <p className="text-slate-600 text-sm mb-4">تمام مکالمات به صورت JSON</p>
          <button 
            onClick={() => handleDownload("/exports/conversations/json", "conversations.json")}
            disabled={loading}
            className="bg-accent hover:bg-accent-hover text-white font-medium px-4 py-2 rounded-xl transition-all text-sm disabled:opacity-50"
          >
            {loading ? "درحال دانلود..." : "دانلود"}
          </button>
        </div>

        <div className="glass-card p-6 hover:bg-white/[0.06] cursor-pointer transition-all">
          <FileJson className="w-8 h-8 text-emerald-400 mb-3" />
          <h3 className="text-white font-medium mb-2">Bookings</h3>
          <p className="text-slate-600 text-sm mb-4">تمام رزرو‌های جلسات</p>
          <button 
            onClick={() => handleDownload("/exports/bookings/json", "bookings.json")}
            disabled={loading}
            className="bg-accent hover:bg-accent-hover text-white font-medium px-4 py-2 rounded-xl transition-all text-sm disabled:opacity-50"
          >
            {loading ? "درحال دانلود..." : "دانلود"}
          </button>
        </div>
      </div>
    </div>
  );
}
