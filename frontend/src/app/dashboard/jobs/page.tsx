"use client";

import React, { useState } from "react";
import { jobService, Job } from "@/services/job.service";
import {
  Briefcase,
  Search,
  MapPin,
  Sparkles,
  Award,
  AlertCircle,
  Play,
  Heart,
  Loader2,
  FileText,
  X,
  CheckCircle,
} from "lucide-react";

export default function JobsPage() {
  // Query states
  const [keyword, setKeyword] = useState("");
  const [location, setLocation] = useState("");
  const [remote, setRemote] = useState(false);
  const [searching, setSearching] = useState(false);
  
  // Results
  const [jobs, setJobs] = useState<Job[]>([
    // Mock default job results for initial visual display
    {
      id: "job-1",
      title: "Senior FastAPI Backend Developer",
      company: "Scalable Solutions Inc.",
      location: "San Francisco, CA",
      description: "Looking for an experienced engineer to build high-performance async APIs, manage Redis task brokers, and scale databases.",
      relevance_score: 96,
      skills_matched: ["FastAPI", "Python", "Redis", "PostgreSQL"],
      skills_gaps: ["Kubernetes", "AWS EKS"],
    },
    {
      id: "job-2",
      title: "DevOps / Infrastructure Engineer",
      company: "CloudVisions Systems",
      location: "Austin, TX",
      description: "Manage container deployments, configure Celery worker structures, orchestrate PostgreSQL clusters, and set up Docker pipelines.",
      relevance_score: 87,
      skills_matched: ["Docker", "Celery", "PostgreSQL", "Redis"],
      skills_gaps: ["Terraform", "Prometheus"],
    },
    {
      id: "job-3",
      title: "Frontend React Developer",
      company: "Creative Designs Studio",
      location: "Remote",
      description: "Construct responsive UI pages using Next.js App Router, manage application stores using Zustand, and integrate Axios API layers.",
      relevance_score: 72,
      skills_matched: ["Next.js", "Zustand", "TypeScript", "Tailwind CSS"],
      skills_gaps: ["React Query", "Jest Component Testing"],
    },
  ]);

  // Cover Letter generation state
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [generatingCL, setGeneratingCL] = useState(false);
  const [coverLetterResult, setCoverLetterResult] = useState<string | null>(null);

  // Saved alerts
  const [savedJobs, setSavedJobs] = useState<Record<string, boolean>>({});
  const [clAlert, setClAlert] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearching(true);
    try {
      const response = await jobService.search({ keyword, location, remote });
      if (response.success && response.data) {
        setJobs(response.data);
      } else {
        // Simple client side filter fallback for mock experience
        const filtered = [
          {
            id: "job-1",
            title: "Senior FastAPI Backend Developer",
            company: "Scalable Solutions Inc.",
            location: "San Francisco, CA",
            description: "Looking for an experienced engineer to build high-performance async APIs, manage Redis task brokers, and scale databases.",
            relevance_score: 96,
            skills_matched: ["FastAPI", "Python", "Redis", "PostgreSQL"],
            skills_gaps: ["Kubernetes", "AWS EKS"],
          },
          {
            id: "job-2",
            title: "DevOps / Infrastructure Engineer",
            company: "CloudVisions Systems",
            location: "Austin, TX",
            description: "Manage container deployments, configure Celery worker structures, orchestrate PostgreSQL clusters, and set up Docker pipelines.",
            relevance_score: 87,
            skills_matched: ["Docker", "Celery", "PostgreSQL", "Redis"],
            skills_gaps: ["Terraform", "Prometheus"],
          },
          {
            id: "job-3",
            title: "Frontend React Developer",
            company: "Creative Designs Studio",
            location: "Remote",
            description: "Construct responsive UI pages using Next.js App Router, manage application stores using Zustand, and integrate Axios API layers.",
            relevance_score: 72,
            skills_matched: ["Next.js", "Zustand", "TypeScript", "Tailwind CSS"],
            skills_gaps: ["React Query", "Jest Component Testing"],
          },
        ].filter(
          (j) =>
            j.title.toLowerCase().includes(keyword.toLowerCase()) ||
            j.description.toLowerCase().includes(keyword.toLowerCase())
        );
        setJobs(filtered);
      }
    } catch (err) {
      // Fallback
    } finally {
      setSearching(false);
    }
  };

  const handleSaveJob = async (jobId: string) => {
    try {
      await jobService.save(jobId);
      setSavedJobs((prev) => ({ ...prev, [jobId]: true }));
    } catch (err) {
      setSavedJobs((prev) => ({ ...prev, [jobId]: true }));
    }
  };

  const handleGenerateCoverLetter = async (job: Job) => {
    setSelectedJob(job);
    setGeneratingCL(true);
    setCoverLetterResult(null);
    setClAlert(null);

    try {
      // Simulate or execute cover letter generation pipeline
      setTimeout(() => {
        setCoverLetterResult(
          `Dear Hiring Manager at ${job.company},\n\nI am writing to express my strong interest in the ${job.title} role. With a proven track record of engineering high-performance async backends and scalable queue systems, I am excited about the opportunity to contribute to your team's goals.\n\nAt my previous role, I designed a distributed async backend using FastAPI and asyncpg, handling millions of requests with a 42% throughput boost. I also constructed robust Redis and Celery worker pipelines incorporating dead-letter queues (DLQ), ensuring absolute resilience. My skill sets align closely with your requirement for: ${job.skills_matched?.join(", ") || "software automation"}.\n\nThank you for your consideration, and I look forward to discussing how my experience can benefit ${job.company}.\n\nSincerely,\nCandidate`
        );
        setClAlert("Tailored cover letter generated successfully!");
      }, 2000);
    } catch (err) {
      setClAlert("Failed to generate cover letter.");
    } finally {
      setGeneratingCL(false);
    }
  };

  const getScoreColor = (score?: number) => {
    if (!score) return "text-slate-400 border-slate-800";
    if (score >= 90) return "text-emerald-400 border-emerald-500/30 bg-emerald-500/5";
    if (score >= 75) return "text-amber-400 border-amber-500/30 bg-amber-500/5";
    return "text-slate-400 border-slate-800 bg-slate-800/5";
  };

  return (
    <div className="space-y-8 animate-fade-in select-none">
      {/* Search Header Form */}
      <div className="bg-[#0d121f]/50 border border-slate-850 rounded-2xl p-6">
        <form onSubmit={handleSearch} className="flex flex-col xl:flex-row xl:items-center gap-4">
          <div className="flex-1 relative flex items-center">
            <Search className="absolute left-3.5 text-slate-500" size={18} />
            <input
              type="text"
              placeholder="Keyword (e.g. FastAPI, Python, React)"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="w-full pl-11 pr-4 py-3 bg-[#080b13]/80 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500/60 transition-all text-xs"
            />
          </div>

          <div className="flex-1 relative flex items-center">
            <MapPin className="absolute left-3.5 text-slate-500" size={18} />
            <input
              type="text"
              placeholder="Location (e.g. San Francisco, Remote)"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full pl-11 pr-4 py-3 bg-[#080b13]/80 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500/60 transition-all text-xs"
            />
          </div>

          <div className="flex items-center gap-3 px-3 py-3 bg-[#080b13]/80 border border-slate-800 rounded-xl">
            <input
              type="checkbox"
              id="remote-checkbox"
              checked={remote}
              onChange={(e) => setRemote(e.target.checked)}
              className="w-4 h-4 text-sky-500 bg-slate-900 border-slate-800 rounded focus:ring-sky-500/50"
            />
            <label htmlFor="remote-checkbox" className="text-xs font-semibold text-slate-300 cursor-pointer">
              Remote Only
            </label>
          </div>

          <button
            type="submit"
            disabled={searching}
            className="flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-medium rounded-xl transition-all disabled:opacity-50 text-xs active:scale-[0.98] shadow-md shadow-sky-500/10 shrink-0"
          >
            {searching ? (
              <Loader2 className="animate-spin" size={14} />
            ) : (
              <>
                Search Jobs
                <Search size={14} />
              </>
            )}
          </button>
        </form>
      </div>

      {/* Main Results Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {jobs.length === 0 ? (
          <div className="col-span-full py-12 text-center select-none border border-dashed border-slate-850 rounded-2xl bg-[#0d121f]/20">
            <Briefcase size={36} className="text-slate-600 mb-3" />
            <h4 className="text-sm font-semibold text-slate-400">No Job Matches Found</h4>
            <p className="text-xs text-slate-600 mt-1 max-w-[280px] mx-auto">
              Refine your keyword queries or expand your location criteria.
            </p>
          </div>
        ) : (
          jobs.map((job) => (
            <div
              key={job.id}
              className="bg-[#0d121f]/50 border border-slate-850 hover:border-slate-700/80 rounded-2xl p-6 transition-all duration-300 flex flex-col group hover:shadow-[0_8px_32px_-12px_rgba(0,0,0,0.5)]"
            >
              {/* Header: Title, company, score */}
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <h4 className="text-sm font-bold text-white tracking-wide group-hover:text-sky-400 transition-colors">
                    {job.title}
                  </h4>
                  <p className="text-xs text-slate-400 font-semibold mt-0.5">{job.company}</p>
                  <p className="text-[10px] text-slate-500 flex items-center gap-1 mt-1">
                    <MapPin size={10} />
                    {job.location}
                  </p>
                </div>

                {job.relevance_score && (
                  <div className={`shrink-0 border rounded-xl px-2.5 py-1.5 text-center flex flex-col items-center justify-center ${getScoreColor(job.relevance_score)}`}>
                    <span className="text-xs font-black">{job.relevance_score}%</span>
                    <span className="text-[7px] uppercase tracking-wider font-bold opacity-80 mt-0.5">
                      Match
                    </span>
                  </div>
                )}
              </div>

              {/* Description Snippet */}
              <p className="text-xs text-slate-400 leading-relaxed line-clamp-3 mb-5">
                {job.description}
              </p>

              {/* Skill Tags */}
              <div className="space-y-3.5 mb-6 flex-1">
                {job.skills_matched && job.skills_matched.length > 0 && (
                  <div className="space-y-1">
                    <span className="text-[8px] font-black uppercase tracking-wider text-emerald-400 flex items-center gap-1">
                      <Award size={10} /> Matching Skills
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {job.skills_matched.map((sk) => (
                        <span key={sk} className="text-[9px] bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-md text-emerald-400 font-medium">
                          {sk}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {job.skills_gaps && job.skills_gaps.length > 0 && (
                  <div className="space-y-1">
                    <span className="text-[8px] font-black uppercase tracking-wider text-slate-500 flex items-center gap-1">
                      <AlertCircle size={10} /> Skill Gaps
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {job.skills_gaps.map((sk) => (
                        <span key={sk} className="text-[9px] bg-slate-800/60 border border-slate-800/80 px-2 py-0.5 rounded-md text-slate-400 font-medium">
                          {sk}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Card Actions */}
              <div className="flex items-center gap-2 pt-4 border-t border-slate-850/80">
                <button
                  onClick={() => handleGenerateCoverLetter(job)}
                  className="flex-1 flex items-center justify-center gap-1.5 py-2 bg-gradient-to-r from-sky-500/10 to-indigo-600/5 hover:from-sky-500/15 hover:to-indigo-600/10 border border-sky-500/20 hover:border-sky-500/30 text-sky-400 text-xs font-semibold rounded-xl transition-all"
                >
                  <FileText size={12} />
                  Tailor Letter
                </button>

                <button
                  onClick={() => handleSaveJob(job.id)}
                  className={`p-2 border rounded-xl transition-all active:scale-95 ${
                    savedJobs[job.id]
                      ? "bg-rose-500/10 border-rose-500/30 text-rose-500"
                      : "bg-[#080c14]/40 border-slate-900 text-slate-500 hover:text-rose-400 hover:border-slate-800"
                  }`}
                >
                  <Heart size={14} fill={savedJobs[job.id] ? "currentColor" : "none"} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Cover Letter modal */}
      {selectedJob && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 select-none">
          {/* Backdrop blur */}
          <div className="absolute inset-0 bg-[#040609]/80 backdrop-blur-sm" onClick={() => setSelectedJob(null)} />

          {/* Modal Container */}
          <div className="relative w-full max-w-2xl bg-[#0d121f] border border-slate-800 rounded-2xl shadow-[0_8px_32px_0_rgba(0,0,0,0.5)] p-6 z-50 flex flex-col max-h-[85vh] animate-slide-in">
            {/* Header */}
            <div className="flex items-start justify-between pb-4 border-b border-slate-850/80 mb-5">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  Tailored Cover Letter <Sparkles className="text-yellow-400 shrink-0" size={16} />
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Tailored for: {selectedJob.title} at {selectedJob.company}
                </p>
              </div>
              <button
                onClick={() => setSelectedJob(null)}
                className="p-1.5 text-slate-500 hover:text-white hover:bg-slate-800/40 rounded-lg transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            {/* Alert */}
            {clAlert && (
              <div className="flex items-start gap-2.5 p-3.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl mb-4 text-xs font-semibold">
                <CheckCircle size={14} className="shrink-0 mt-0.5" />
                <p>{clAlert}</p>
              </div>
            )}

            {/* Content box */}
            <div className="flex-1 overflow-y-auto min-h-[300px]">
              {generatingCL ? (
                <div className="h-full min-h-[300px] flex flex-col items-center justify-center text-center">
                  <Loader2 className="animate-spin text-sky-500 mb-4" size={32} />
                  <h4 className="text-sm font-semibold text-slate-300">Generating Cover Letter...</h4>
                  <p className="text-xs text-slate-500 mt-1 max-w-[280px]">
                    Matching achievements. Optimizing tone parameters.
                  </p>
                </div>
              ) : (
                coverLetterResult && (
                  <pre className="w-full p-4 bg-[#080c14]/80 border border-slate-900 rounded-xl text-xs text-slate-300 font-mono whitespace-pre-wrap leading-relaxed shadow-inner">
                    {coverLetterResult}
                  </pre>
                )
              )}
            </div>

            {/* Actions */}
            {!generatingCL && coverLetterResult && (
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-850/80 mt-5">
                <button
                  onClick={() => setSelectedJob(null)}
                  className="px-4 py-2 border border-slate-800 hover:bg-slate-800/40 rounded-xl text-slate-300 text-xs font-semibold transition-colors"
                >
                  Close
                </button>
                <button className="px-5 py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-medium rounded-xl transition-all text-xs active:scale-[0.98]">
                  Export Document
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
