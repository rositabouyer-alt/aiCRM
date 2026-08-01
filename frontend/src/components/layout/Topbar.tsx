"use client";
import { Bell, Search, RefreshCw } from "lucide-react";

export default function Topbar() {
  return (
    <header className="h-16 border-b border-pink-500/10 bg-[#0a0a0a]/80 backdrop-blur-sm flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center gap-3 flex-1 max-w-md">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-600" />
          <input type="text" placeholder="Search leads, conversations..." className="input-dark pl-9" />
        </div>
      </div>
      <div className="flex items-center gap-2">
        <button className="btn-ghost"><RefreshCw className="w-4 h-4" /></button>
        <button className="relative btn-ghost">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-accent rounded-full" />
        </button>
        <div className="w-px h-6 bg-white/10 mx-1" />
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
          All systems online
        </div>
      </div>
    </header>
  );
}
