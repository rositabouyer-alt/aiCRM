"use client";
import { Settings, Key, Bell, Shield, Zap } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <h1 className="text-xl font-semibold text-white flex items-center gap-2">
        <Settings className="w-5 h-5 text-accent" />
        تنظیمات
      </h1>

      {/* API Keys */}
      <div className="glass-card p-6">
        <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
          <Key className="w-4 h-4 text-accent" />
          API Keys
        </h2>
        <div className="space-y-4">
          <div>
            <label className="text-slate-400 text-sm block mb-2">Telegram Bot Token</label>
            <input type="password" value="8884657674:AAHFy..." className="input-dark" disabled />
          </div>
          <div>
            <label className="text-slate-400 text-sm block mb-2">Instagram Access Token</label>
            <input type="password" placeholder="هنوز تنظیم نشده" className="input-dark" />
          </div>
          <button className="btn-primary text-sm">Save</button>
        </div>
      </div>

      {/* Integrations */}
      <div className="glass-card p-6">
        <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
          <Zap className="w-4 h-4 text-accent" />
          انتگریشن‌ها
        </h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-white/[0.02] rounded-lg">
            <span className="text-white text-sm">Telegram</span>
            <span className="text-emerald-400 text-xs">✓ فعال</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-white/[0.02] rounded-lg">
            <span className="text-white text-sm">Instagram</span>
            <span className="text-slate-500 text-xs">غیرفعال</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-white/[0.02] rounded-lg">
            <span className="text-white text-sm">WhatsApp</span>
            <span className="text-slate-500 text-xs">غیرفعال</span>
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="glass-card p-6">
        <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
          <Bell className="w-4 h-4 text-accent" />
          اعلان‌ها
        </h2>
        <div className="space-y-3">
          <label className="flex items-center gap-3">
            <input type="checkbox" defaultChecked className="w-4 h-4" />
            <span className="text-slate-400 text-sm">پیام‌های جدید</span>
          </label>
          <label className="flex items-center gap-3">
            <input type="checkbox" defaultChecked className="w-4 h-4" />
            <span className="text-slate-400 text-sm">لیدهای جدید</span>
          </label>
          <label className="flex items-center gap-3">
            <input type="checkbox" defaultChecked className="w-4 h-4" />
            <span className="text-slate-400 text-sm">بوکینگ‌های جدید</span>
          </label>
        </div>
      </div>
    </div>
  );
}
