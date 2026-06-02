"use client";

import React from "react";
import { useAuthStore } from "@/stores/authStore";
import {
  FileText,
  Briefcase,
  GitBranch,
  CheckCircle,
  AlertTriangle,
  Play,
  ArrowRight,
  TrendingUp,
  Clock,
  Sparkles,
} from "lucide-react";

export default function DashboardOverviewPage() {
  const { user } = useAuthStore();

  const metrics = [
    {
      name: "Resumes Optimized",
      value: "12",
      change: "+2 this week",
      icon: FileText,
      color: "from-sky-500 to-sky-600",
      glow: "rgba(14,165,233,0.15)",
    },
    {
      name: "Jobs Aggregated",
      value: "148",
      change: "48 new matches",
      icon: Briefcase,
      color: "from-indigo-500 to-indigo-600",
      glow: "rgba(99,102,241,0.15)",
    },
    {
      name: "Workflows Executed",
      value: "37",
      change: "100% success rate",
      icon: GitBranch,
      color: "from-purple-500 to-purple-600",
      glow: "rgba(168,85,247,0.15)",
    },
    {
      name: "Average ATS Score",
      value: "94%",
      change: "+5% improvement",
      icon: TrendingUp,
      color: "from-emerald-500 to-emerald-600",
      glow: "rgba(16,185,129,0.15)",
    },
  ];

  const recentWorkflows = [
    {
      id: "wf-101",
      name: "Resume Optimization Chain",
      user: "user@example.com",
      status: "completed",
      time: "10 mins ago",
      queue: "ai_tasks",
    },
    {
      id: "wf-102",
      name: "Aggregated Job scraping pipeline",
      user: "user@example.com",
      status: "completed",
      time: "1 hour ago",
      queue: "scraping",
    },
    {
      id: "wf-103",
      name: "Webhook Delivery callback",
      user: "fail@example.com",
      status: "failed",
      time: "3 hours ago",
      queue: "dead_letter",
      error: "Connection timed out permanently after 6 retries",
    },
    {
      id: "wf-104",
      name: "Consensus AI cover letter",
      user: "user@example.com",
      status: "retrying",
      time: "Just now",
      queue: "ai_tasks",
    },
  ];

  return (
    <div className="space-y-8 animate-fade-in select-none">
      {/* Greetings Banner */}
      <div className="relative p-6 lg:p-8 bg-gradient-to-r from-[#0e1629] to-[#0d121f] border border-slate-800/80 rounded-2xl overflow-hidden shadow-[0_8px_32px_0_rgba(0,0,0,0.3)]">
        <div className="absolute top-0 right-0 w-[300px] h-[300px] bg-[radial-gradient(circle_at_center,rgba(56,189,248,0.05)_0,transparent_60%)] filter blur-3xl" />
        <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-6">
          <div className="space-y-1.5">
            <h1 className="text-xl lg:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Welcome back, {user?.full_name || "Seeker"}! <Sparkles className="text-yellow-400 shrink-0" size={20} />
            </h1>
            <p className="text-sm text-slate-400 max-w-xl leading-relaxed">
              Your autonomous AI job applications engine is running smoothly. Upload a new resume or configure custom automated pipelines.
            </p>
          </div>
          <button className="sm:self-center shrink-0 flex items-center justify-center gap-2 px-5 py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-medium rounded-xl transition-all shadow-[0_4px_14px_rgba(14,165,233,0.25)] hover:shadow-[0_6px_20px_rgba(14,165,233,0.35)] active:scale-[0.98]">
            Configure Pipeline
            <ArrowRight size={16} />
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div
              key={metric.name}
              className="relative bg-[#0d121f]/50 border border-slate-850 rounded-2xl p-6 transition-all duration-300 hover:border-slate-750 group hover:shadow-[0_8px_32px_-12px_rgba(0,0,0,0.5)] overflow-hidden"
              style={{
                boxShadow: `inset 0 -1px 20px 0 ${metric.glow}`,
              }}
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  {metric.name}
                </span>
                <div className={`p-2.5 rounded-xl bg-gradient-to-br ${metric.color} text-white shadow-md shadow-black/20 group-hover:scale-105 transition-transform`}>
                  <Icon size={18} />
                </div>
              </div>
              <h3 className="text-3xl font-extrabold tracking-tight text-white mb-1">
                {metric.value}
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                {metric.change}
              </p>
            </div>
          );
        })}
      </div>

      {/* Bottom Layout - Recent Activity and Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Workflows */}
        <div className="lg:col-span-2 bg-[#0d121f]/50 border border-slate-850 rounded-2xl p-6 flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <div className="space-y-0.5">
              <h3 className="text-base font-bold text-white tracking-wide">
                Recent Queue Executions
              </h3>
              <p className="text-xs text-slate-500">
                Track async worker pipelines and dead-letter statuses
              </p>
            </div>
            <button className="text-xs text-sky-400 hover:text-sky-300 font-semibold transition-colors flex items-center gap-1">
              View all
              <ArrowRight size={12} />
            </button>
          </div>

          <div className="space-y-4 flex-1">
            {recentWorkflows.map((wf) => (
              <div
                key={wf.id}
                className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-[#080c14]/60 border border-slate-900 rounded-xl hover:border-slate-800 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <div className={`mt-0.5 p-2 rounded-lg shrink-0 ${
                    wf.status === "completed"
                      ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                      : wf.status === "failed"
                      ? "bg-red-500/10 text-red-400 border border-red-500/20"
                      : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                  }`}>
                    {wf.status === "completed" ? (
                      <CheckCircle size={14} />
                    ) : (
                      <AlertTriangle size={14} />
                    )}
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-200">
                      {wf.name}
                    </h4>
                    <div className="flex flex-wrap items-center gap-2 mt-1">
                      <span className="text-[10px] bg-slate-800/60 px-1.5 py-0.5 rounded text-slate-400 uppercase tracking-wide font-semibold">
                        {wf.queue}
                      </span>
                      <span className="text-[10px] text-slate-500 flex items-center gap-1">
                        <Clock size={10} />
                        {wf.time}
                      </span>
                    </div>
                    {wf.error && (
                      <p className="text-xs text-red-400/80 mt-1.5 font-mono">
                        Error: {wf.error}
                      </p>
                    )}
                  </div>
                </div>
                <div className="self-end sm:self-center shrink-0">
                  <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold uppercase tracking-wide ${
                    wf.status === "completed"
                      ? "bg-emerald-500/10 text-emerald-400"
                      : wf.status === "failed"
                      ? "bg-red-500/10 text-red-400"
                      : "bg-amber-500/10 text-amber-400"
                  }`}>
                    {wf.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-[#0d121f]/50 border border-slate-850 rounded-2xl p-6 space-y-6">
          <div>
            <h3 className="text-base font-bold text-white tracking-wide">
              Quick Actions
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Launch manual processing triggers
            </p>
          </div>

          <div className="space-y-3">
            <button className="w-full flex items-center justify-between p-4 bg-gradient-to-r from-sky-500/10 to-indigo-500/5 hover:from-sky-500/15 hover:to-indigo-500/10 border border-sky-500/20 hover:border-sky-500/30 rounded-xl text-left transition-all duration-200 group active:scale-[0.98]">
              <div>
                <h4 className="text-sm font-bold text-sky-400 flex items-center gap-1.5">
                  Optimize Resume <Sparkles size={14} />
                </h4>
                <p className="text-xs text-slate-400 mt-0.5">
                  Parse and align bullet points using STAR method
                </p>
              </div>
              <div className="p-2 bg-sky-500/10 rounded-lg text-sky-400 group-hover:translate-x-0.5 transition-transform">
                <Play size={12} fill="currentColor" />
              </div>
            </button>

            <button className="w-full flex items-center justify-between p-4 bg-[#080c14]/60 border border-slate-850 hover:border-slate-700 rounded-xl text-left transition-all duration-200 group active:scale-[0.98]">
              <div>
                <h4 className="text-sm font-bold text-slate-200">
                  Scrape New Jobs
                </h4>
                <p className="text-xs text-slate-500 mt-0.5">
                  Aggregate matches for FastAPI in San Francisco
                </p>
              </div>
              <div className="p-2 bg-slate-800 rounded-lg text-slate-400 group-hover:translate-x-0.5 transition-transform">
                <Play size={12} fill="currentColor" />
              </div>
            </button>

            <button className="w-full flex items-center justify-between p-4 bg-[#080c14]/60 border border-slate-850 hover:border-slate-700 rounded-xl text-left transition-all duration-200 group active:scale-[0.98]">
              <div>
                <h4 className="text-sm font-bold text-slate-200">
                  Trigger Mock Failure
                </h4>
                <p className="text-xs text-slate-500 mt-0.5">
                  Run permanent failure webhook chain to trigger DLQ
                </p>
              </div>
              <div className="p-2 bg-slate-800 rounded-lg text-slate-400 group-hover:translate-x-0.5 transition-transform">
                <Play size={12} fill="currentColor" />
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
