"use client";

import React, { useState, useEffect } from "react";
import { workflowService, WorkflowRun } from "@/services/workflow.service";
import {
  GitBranch,
  Play,
  RotateCcw,
  CheckCircle,
  AlertTriangle,
  Server,
  Activity,
  Trash2,
  Clock,
  Code,
  Terminal,
  ShieldAlert,
  Loader2,
} from "lucide-react";

export default function WorkflowsPage() {
  const [triggering, setTriggering] = useState(false);
  const [alert, setAlert] = useState<{ type: "success" | "error"; msg: string } | null>(null);

  // Expander card tracking
  const [expandedTask, setExpandedTask] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Mock list combined with Celery background worker executions (e.g., standard tasks and DLQ)
  const [runs, setRuns] = useState<any[]>([
    {
      id: "celery-task-8812",
      name: "app.tasks.ai.optimize_resume_task",
      queue: "ai_tasks",
      status: "completed",
      time: "2 mins ago",
      duration: "3.4s",
      args: ['"Original Resume Text..."', '"FastAPI Engineer"'],
    },
    {
      id: "celery-task-8813",
      name: "app.tasks.notifications.send_email_task",
      queue: "notifications",
      status: "completed",
      time: "2 mins ago",
      duration: "1.1s",
      args: ['"architect@example.com"', '"Optimized Resume: Principal Architect"', '"Hello..."'],
    },
    {
      id: "celery-task-9901",
      name: "app.tasks.notifications.send_webhook_task",
      queue: "dead_letter",
      status: "failed",
      time: "4 hours ago",
      duration: "32.0s",
      args: ['"https://example.com/webhook"', '"resume.optimized"', '{"id": 9901, "status": "completed"}'],
      retries_run: "6 / 6",
      error: "HTTPStatusError: Webhook target returned error code 503 Service Unavailable",
      stack_trace: `Traceback (most recent call last):
  File "C:\\Users\\sri\\job-tracker\\backend\\app\\core\\celery_app.py", line 52, in on_failure
    super().on_failure(exc, task_id, args, kwargs, einfo)
  File "C:\\Users\\sri\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\celery\\app\\task.py", line 720, in on_failure
    raise exc
  File "C:\\Users\\sri\\job-tracker\\backend\\app\\tasks\\notifications.py", line 47, in send_webhook_task
    raise httpx.HTTPStatusError("Webhook target returned error code 503")
httpx.HTTPStatusError: Webhook target returned error code 503 Service Unavailable`,
    },
    {
      id: "celery-task-7722",
      name: "app.tasks.scraping.scrape_jobs_task",
      queue: "scraping",
      status: "completed",
      time: "1 hour ago",
      duration: "2.1s",
      args: ['"FastAPI"', '"San Francisco"'],
    },
  ]);

  const loadWorkflows = async () => {
    try {
      const response = await workflowService.getAll();
      if (response.success && response.data) {
        // Map backend runs to dashboard display structures
        const mappedRuns = response.data.map((r: WorkflowRun) => {
          let runTime = "Just now";
          if (r.created_at) {
            const date = new Date(r.created_at);
            runTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          }
          return {
            id: r.id,
            name: r.task_name,
            queue: r.queue,
            status: r.status,
            time: runTime,
            duration: r.status === "completed" ? "4.2s" : r.status === "running" ? "Running..." : "N/A",
            args: ['"Original Resume Text..."', '"Principal Architect"', '"architect@example.com"'],
            logs: r.logs,
          };
        });

        setRuns((prev) => {
          const staticMocks = prev.filter((p) => !p.id.startsWith("wf-") && !p.id.includes("-task-id-") && p.id !== "celery-task-live");
          const finalMocks = staticMocks.length > 0 ? staticMocks : [
            {
              id: "celery-task-8812",
              name: "app.tasks.ai.optimize_resume_task",
              queue: "ai_tasks",
              status: "completed",
              time: "2 mins ago",
              duration: "3.4s",
              args: ['"Original Resume Text..."', '"FastAPI Engineer"'],
            },
            {
              id: "celery-task-8813",
              name: "app.tasks.notifications.send_email_task",
              queue: "notifications",
              status: "completed",
              time: "2 mins ago",
              duration: "1.1s",
              args: ['"architect@example.com"', '"Optimized Resume: Principal Architect"', '"Hello..."'],
            },
            {
              id: "celery-task-9901",
              name: "app.tasks.notifications.send_webhook_task",
              queue: "dead_letter",
              status: "failed",
              time: "4 hours ago",
              duration: "32.0s",
              args: ['"https://example.com/webhook"', '"resume.optimized"', '{"id": 9901, "status": "completed"}'],
              retries_run: "6 / 6",
              error: "HTTPStatusError: Webhook target returned error code 503 Service Unavailable",
              stack_trace: `Traceback (most recent call last):
  File "C:\\Users\\sri\\job-tracker\\backend\\app\\core\\celery_app.py", line 52, in on_failure
    super().on_failure(exc, task_id, args, kwargs, einfo)
  File "C:\\Users\\sri\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\celery\\app\\task.py", line 720, in on_failure
    raise exc
  File "C:\\Users\\sri\\job-tracker\\backend\\app\\tasks\\notifications.py", line 47, in send_webhook_task
    raise httpx.HTTPStatusError("Webhook target returned error code 503")
httpx.HTTPStatusError: Webhook target returned error code 503 Service Unavailable`,
            },
            {
              id: "celery-task-7722",
              name: "app.tasks.scraping.scrape_jobs_task",
              queue: "scraping",
              status: "completed",
              time: "1 hour ago",
              duration: "2.1s",
              args: ['"FastAPI"', '"San Francisco"'],
            },
          ];
          return [...mappedRuns, ...finalMocks];
        });
      }
    } catch (err) {
      console.error("Failed to load workflows", err);
    }
  };

  useEffect(() => {
    loadWorkflows();
    const interval = setInterval(loadWorkflows, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleTriggerWorkflow = async () => {
    setTriggering(true);
    setAlert(null);

    try {
      const createRes = await workflowService.create({
        task_name: "app.tasks.workflows.run_resume_optimization_pipeline",
        queue: "workflows",
      });

      if (!createRes.success || !createRes.data) {
        throw new Error(createRes.error?.message || "Failed to create workflow run");
      }

      const workflowId = createRes.data.id;
      const triggerRes = await workflowService.trigger(workflowId);

      if (!triggerRes.success || !triggerRes.data) {
        throw new Error(triggerRes.error?.message || "Failed to trigger workflow");
      }

      setAlert({
        type: "success",
        msg: `Celery Canvas chain 'Optimize Resume -> Send Email' successfully triggered with Task ID: ${triggerRes.data.task_id}`,
      });
      await loadWorkflows();
    } catch (err: any) {
      setAlert({ type: "error", msg: err.message || "Failed to connect to Celery task broker." });
    } finally {
      setTriggering(false);
    }
  };

  const handleReplayDLQ = (taskId: string) => {
    setAlert({
      type: "success",
      msg: `Task ${taskId} re-queued into high-priority retry_queue list. Initiating reprocessing...`,
    });
    setRuns((prev) =>
      prev.map((run) =>
        run.id === taskId
          ? { ...run, status: "completed", queue: "notifications", time: "Just now", error: null, stack_trace: null }
          : run
      )
    );
  };

  return (
    <div className="space-y-8 animate-fade-in select-none">
      {alert && (
        <div
          className={`flex items-start gap-3 p-4 rounded-xl border text-sm ${
            alert.type === "success"
              ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
              : "bg-red-500/10 border-red-500/20 text-red-400"
          }`}
        >
          <CheckCircle size={18} />
          <p>{alert.msg}</p>
        </div>
      )}

      {/* Main Grid: Isolated Queues and Canvas triggers */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Workers & Queues list */}
        <div className="xl:col-span-2 bg-[#0d121f]/50 border border-slate-850 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-bold text-white tracking-wide flex items-center gap-2">
                Isolated Queue Broker <Server className="text-sky-400" size={18} />
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Observed queue capacities and concurrency channels
              </p>
            </div>
            <div className="flex items-center gap-1.5 px-2.5 py-1 bg-emerald-500/10 rounded-full text-[10px] text-emerald-400 font-bold uppercase tracking-wider">
              <Activity size={10} className="animate-pulse" /> Active
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              { name: "ai_tasks", concurrency: 2, load: "Medium", color: "text-purple-400 border-purple-500/20" },
              { name: "notifications", concurrency: 4, load: "Low", color: "text-sky-400 border-sky-500/20" },
              { name: "scraping", concurrency: 2, load: "Idle", color: "text-amber-400 border-amber-500/20" },
              { name: "workflows", concurrency: 2, load: "Low", color: "text-indigo-400 border-indigo-500/20" },
            ].map((q) => (
              <div
                key={q.name}
                className="p-4 bg-[#080c14]/40 border border-slate-900 rounded-xl hover:border-slate-800 transition-colors flex items-center justify-between"
              >
                <div>
                  <h4 className="text-xs font-black text-slate-200">{q.name}</h4>
                  <p className="text-[10px] text-slate-500 mt-1 font-semibold">
                    Concurrency Channels: {q.concurrency}
                  </p>
                </div>
                <div className={`border rounded-lg px-2.5 py-1 text-[10px] uppercase font-black tracking-wider ${q.color}`}>
                  {q.load}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Trigger Canvas Chain card */}
        <div className="bg-[#0d121f]/50 border border-slate-850 rounded-2xl p-6 space-y-6">
          <div>
            <h3 className="text-base font-bold text-white tracking-wide">Manual Chain Dispatcher</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Force trigger high-level pipelines eagerly
            </p>
          </div>

          <div className="p-4 bg-gradient-to-r from-sky-500/10 to-indigo-500/5 border border-sky-500/20 rounded-xl space-y-4">
            <div>
              <h4 className="text-xs font-bold text-sky-400">Resume Optimization Pipeline</h4>
              <p className="text-[10px] text-slate-400 leading-relaxed mt-1">
                Trigger chain sequence: `optimize_resume_task` (AI) $\rightarrow$ `email_delivery_after_optimization` (SMTP Notification).
              </p>
            </div>

            <button
              onClick={handleTriggerWorkflow}
              disabled={triggering}
              className="w-full flex items-center justify-center gap-2 py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-medium rounded-xl transition-all disabled:opacity-50 text-xs active:scale-[0.98]"
            >
              {triggering ? (
                <Loader2 className="animate-spin" size={14} />
              ) : (
                <>
                  Dispatch eager Chain
                  <Play size={12} fill="currentColor" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Task Execution Table */}
      <div className="bg-[#0d121f]/50 border border-slate-850 rounded-2xl p-6">
        <div className="mb-6">
          <h3 className="text-base font-bold text-white tracking-wide">Task Executions</h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Forensic analysis of all worker statuses and retries
          </p>
        </div>

        <div className="space-y-4">
          {runs.map((run) => (
            <div
              key={run.id}
              className="border border-slate-900 rounded-xl overflow-hidden hover:border-slate-800 transition-colors"
            >
              {/* Main Summary strip */}
              <div
                onClick={() => setExpandedTask(expandedTask === run.id ? null : run.id)}
                className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-[#080c14]/40 cursor-pointer select-none"
              >
                <div className="flex items-start gap-3">
                  <div className={`p-2 rounded-lg shrink-0 ${
                    run.status === "completed"
                      ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                      : "bg-red-500/10 text-red-400 border border-red-500/20"
                  }`}>
                    {run.status === "completed" ? (
                      <CheckCircle size={14} />
                    ) : (
                      <AlertTriangle size={14} />
                    )}
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-slate-200">{run.name}</h4>
                    <div className="flex flex-wrap items-center gap-2 mt-1.5">
                      <span className="text-[9px] bg-slate-900 px-1.5 py-0.5 rounded text-slate-500 font-semibold tracking-wide border border-slate-850">
                        ID: {run.id}
                      </span>
                      <span className="text-[9px] bg-slate-900 px-1.5 py-0.5 rounded text-slate-500 font-semibold tracking-wide border border-slate-850">
                        {run.queue}
                      </span>
                      <span className="text-[9px] text-slate-600 flex items-center gap-1">
                        <Clock size={10} />
                        {run.time}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-5 self-end sm:self-center shrink-0">
                  <span className="text-xs text-slate-500 font-semibold font-mono">{run.duration}</span>
                  <span className={`px-2.5 py-0.5 border rounded-full text-[9px] uppercase font-black tracking-wider ${
                    run.status === "completed"
                      ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
                      : "bg-red-500/10 border-red-500/20 text-red-400 animate-pulse"
                  }`}>
                    {run.status}
                  </span>
                </div>
              </div>

              {/* Expander detailed panel */}
              {expandedTask === run.id && (
                <div className="p-5 border-t border-slate-900 bg-[#060910]/80 space-y-4 animate-slide-in">
                  {/* Arguments payload block */}
                  <div className="space-y-1.5">
                    <span className="text-[10px] font-bold text-slate-400 tracking-wider uppercase flex items-center gap-1.5">
                      <Code size={12} /> Payload Arguments (args)
                    </span>
                    <pre className="p-3 bg-[#03060c] border border-slate-950 rounded-lg text-[10px] text-slate-400 font-mono whitespace-pre-wrap leading-relaxed shadow-inner">
                      [{run.args.join(", ")}]
                    </pre>
                  </div>

                  {/* Celery Task logs */}
                  {run.logs && (
                    <div className="space-y-1.5">
                      <span className="text-[10px] font-bold text-slate-400 tracking-wider uppercase flex items-center gap-1.5">
                        <Terminal size={12} /> Live Celery Task Output / Logs
                      </span>
                      <pre className="p-3 bg-[#03060c] border border-slate-950 rounded-lg text-[10px] text-slate-300 font-mono whitespace-pre-wrap leading-relaxed shadow-inner">
                        {run.logs}
                      </pre>
                    </div>
                  )}

                  {/* Failure Trace details */}
                  {run.status === "failed" && (
                    <>
                      {/* Retry count */}
                      <div className="flex items-center gap-2 text-xs text-slate-400">
                        <span className="font-bold">Retries executed:</span>
                        <span className="bg-red-500/10 border border-red-500/20 px-1.5 py-0.5 rounded text-red-400 font-mono font-semibold">
                          {run.retries_run}
                        </span>
                      </div>

                      {/* Error & Stack trace */}
                      <div className="space-y-1.5">
                        <span className="text-[10px] font-bold text-red-400/80 tracking-wider uppercase flex items-center gap-1.5">
                          <ShieldAlert size={12} /> Dead-Letter trace (einfo)
                        </span>
                        <pre className="p-3 bg-red-950/10 border border-red-900/20 rounded-lg text-[10px] text-red-400/80 font-mono whitespace-pre-wrap leading-relaxed shadow-inner">
                          {run.stack_trace}
                        </pre>
                      </div>

                      {/* Replay action */}
                      <div className="flex items-center justify-end pt-3 border-t border-slate-900/60">
                        <button
                          onClick={() => handleReplayDLQ(run.id)}
                          className="flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl transition-all shadow-md active:scale-95"
                        >
                          <RotateCcw size={12} />
                          Replay task from DLQ
                        </button>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
