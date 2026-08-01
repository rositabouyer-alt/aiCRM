"use client";
import { usePathname } from "next/navigation";
import Link from "next/link";
import {
  LayoutDashboard, Users, MessageSquare, CalendarCheck,
  Phone, BarChart3, Download, Settings, Zap
} from "lucide-react";
import { clsx } from "clsx";

const navItems = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/dashboard/leads", icon: Users, label: "Leads" },
  { href: "/dashboard/conversations", icon: MessageSquare, label: "Conversations" },
  { href: "/dashboard/bookings", icon: CalendarCheck, label: "Bookings" },
  { href: "/dashboard/calls", icon: Phone, label: "Calls" },
  { href: "/dashboard/analytics", icon: BarChart3, label: "Analytics" },
  { href: "/dashboard/downloads", icon: Download, label: "Downloads" },
  { href: "/dashboard/settings", icon: Settings, label: "Settings" },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="w-64 h-screen bg-[#0a0a0a] border-r border-pink-500/10 flex flex-col fixed left-0 top-0 z-30">
      {/* Logo */}
      <div className="p-6 border-b border-pink-500/10">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-accent/10 border border-accent/30 flex items-center justify-center text-accent font-bold text-lg">
            R
          </div>
          <div>
            <p className="text-white font-semibold text-sm">Rozita</p>
            <p className="text-slate-600 text-xs">AI Platform</p>
          </div>
        </div>
      </div>

      {/* AI Status */}
      <div className="px-4 py-3 mx-3 mt-4 glass-card flex items-center gap-2.5">
        <div className="w-2 h-2 rounded-full bg-accent animate-pulse-slow" />
        <span className="text-xs text-slate-400 font-medium">AI Assistant Active</span>
        <Zap className="w-3.5 h-3.5 text-accent ml-auto" />
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map(({ href, icon: Icon, label }) => {
          const isActive = pathname === href || (href !== "/dashboard" && pathname.startsWith(href));
          return (
            <Link key={href} href={href}>
              <div className={clsx(isActive ? "sidebar-item-active" : "sidebar-item-inactive")}>
                <Icon size={18} className="shrink-0" />
                <span>{label}</span>
                {label === "Conversations" && (
                  <span className="ml-auto bg-accent text-white text-xs px-1.5 py-0.5 rounded-full">3</span>
                )}
              </div>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-pink-500/10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-accent to-violet-500 flex items-center justify-center text-white text-xs font-bold">
            R
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-white text-xs font-medium truncate">Rozita</p>
            <p className="text-slate-600 text-xs truncate">rozita@aicrm.io</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
