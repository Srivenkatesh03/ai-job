"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import {
  LayoutDashboard,
  FileText,
  Briefcase,
  GitBranch,
  Bell,
  LogOut,
  Menu,
  X,
  Workflow,
  Settings,
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navLinks = [
    { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
    { name: "Resumes", href: "/dashboard/resumes", icon: FileText },
    { name: "Jobs", href: "/dashboard/jobs", icon: Briefcase },
    { name: "Workflows", href: "/dashboard/workflows", icon: GitBranch },
    { name: "Notifications", href: "/dashboard/notifications", icon: Bell },
  ];

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  const getInitials = (name?: string) => {
    if (!name) return "U";
    return name
      .split(" ")
      .map((part) => part[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-[#0d121f]/90 border-r border-slate-800/80 backdrop-blur-xl p-5 select-none">
      {/* Brand Logo */}
      <div className="flex items-center gap-3 mb-10 px-2 py-1">
        <div className="p-2 bg-gradient-to-r from-sky-500 to-indigo-600 rounded-xl text-white">
          <Workflow size={22} />
        </div>
        <span className="text-lg font-bold tracking-wider bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
          AI JOB SUITE
        </span>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 space-y-1.5">
        {navLinks.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href;

          return (
            <Link
              key={link.name}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className={`flex items-center gap-3.5 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group ${
                isActive
                  ? "bg-gradient-to-r from-sky-500/15 to-indigo-600/10 border border-sky-500/30 text-sky-400 shadow-[0_4px_20px_rgba(14,165,233,0.05)]"
                  : "text-slate-400 border border-transparent hover:bg-slate-800/30 hover:text-slate-200"
              }`}
            >
              <Icon
                size={18}
                className={`transition-transform duration-200 group-hover:scale-105 ${
                  isActive ? "text-sky-400" : "text-slate-500 group-hover:text-slate-300"
                }`}
              />
              {link.name}
            </Link>
          );
        })}
      </nav>

      {/* User profile and logout */}
      <div className="border-t border-slate-800/80 pt-5 mt-auto space-y-4">
        <div className="flex items-center gap-3 px-2">
          {/* Initials Avatar */}
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-sky-500/20 to-indigo-500/20 border border-sky-500/40 flex items-center justify-center font-bold text-sm text-sky-400 shadow-md shadow-sky-500/5">
            {getInitials(user?.full_name)}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-white truncate">
              {user?.full_name || "Active User"}
            </p>
            <p className="text-xs text-slate-500 truncate capitalize">
              Role: {user?.role || "User"}
            </p>
          </div>
        </div>

        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 border border-red-500/20 hover:bg-red-500/5 text-red-400 rounded-xl text-sm font-medium transition-all group active:scale-[0.98]"
        >
          <LogOut size={18} className="transition-transform group-hover:translate-x-0.5" />
          Sign Out
        </button>
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile Toggle Button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-2.5 bg-[#0d121f]/90 border border-slate-800 rounded-xl text-slate-300 hover:text-white"
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Desktop Sidebar */}
      <div className="hidden lg:block w-64 h-full shrink-0">
        <SidebarContent />
      </div>

      {/* Mobile Drawer Overlay */}
      {mobileOpen && (
        <div className="lg:hidden fixed inset-0 z-40 flex">
          {/* Backdrop blur */}
          <div
            className="fixed inset-0 bg-[#040609]/80 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />

          {/* Drawer sheet */}
          <div className="relative w-64 h-full z-50 animate-slide-in">
            <SidebarContent />
          </div>
        </div>
      )}
    </>
  );
}
