"use client";

import React from "react";
import { usePathname } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { Bell, Shield, Server, RefreshCw } from "lucide-react";

export function Header() {
  const pathname = usePathname();
  const { user } = useAuthStore();

  const getPageTitle = (path: string) => {
    if (path.includes("/resumes")) return "Resume Optimization";
    if (path.includes("/jobs")) return "Job Discovery Automation";
    if (path.includes("/workflows")) return "Workflow Orchestrator";
    if (path.includes("/notifications")) return "Alerts & Notifications";
    return "Overview Dashboard";
  };

  return (
    <header className="h-16 shrink-0 bg-[#0d121f]/50 border-b border-slate-800/80 backdrop-blur-xl flex items-center justify-between px-6 lg:px-8 select-none">
      {/* Title block */}
      <div className="flex items-center gap-3">
        {/* Responsive margin for mobile nav toggle spacing */}
        <div className="w-10 h-10 lg:hidden shrink-0" />
        <h2 className="text-lg font-bold text-white font-sans tracking-wide">
          {getPageTitle(pathname)}
        </h2>
      </div>

      {/* System Status and Profile */}
      <div className="flex items-center gap-5">
        {/* Status Indicators */}
        <div className="hidden sm:flex items-center gap-3 px-3 py-1.5 bg-[#080b13]/80 border border-slate-800/60 rounded-xl">
          <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            API Offline/SQLite
          </div>
          <span className="text-slate-700">|</span>
          <div className="flex items-center gap-1.5 text-xs text-sky-400 font-medium">
            <Server size={12} />
            Eager Queue
          </div>
        </div>

        {/* Action icons */}
        <div className="flex items-center gap-2">
          <button className="relative p-2 text-slate-400 hover:text-white hover:bg-slate-800/40 rounded-xl transition-all">
            <Bell size={18} />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-sky-500" />
          </button>
        </div>

        {/* Divider */}
        <span className="w-[1px] h-6 bg-slate-800" />

        {/* Header Profile Details */}
        <div className="flex items-center gap-3">
          <div className="text-right hidden md:block">
            <p className="text-xs font-semibold text-white">
              {user?.full_name || "Active User"}
            </p>
            <p className="text-[10px] text-slate-500 tracking-wider uppercase font-bold mt-0.5">
              {user?.role || "standard"}
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}
