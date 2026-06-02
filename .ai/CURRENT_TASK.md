# CURRENT_TASK.md

## Current Goal

Implement Phase 5 — Frontend Dashboard Feature Sub-Views.

---

## Scope

* Build dynamic Resume Optimizer upload and review panels (`src/app/dashboard/resumes/page.tsx`):
  * Drag-and-drop PDF/DOCX file uploader with max 10MB bounds.
  * AI suggestions parsing list.
  * Score dashboard progress meter.
* Build Job Search Match Grid list panels (`src/app/dashboard/jobs/page.tsx`):
  * Filter query strings by title keyword, locations, remote options.
  * Semantic match score indicators (HSL tailored color bands).
  * Skill lists matched vs gaps.
  * Modal dialog generating live customized cover letters using AI fallback pipelines.
* Build Workflow Orchestrator status monitor panel (`src/app/dashboard/workflows/page.tsx`):
  * Celery background queue lists (`ai_tasks`, `notifications`, `scraping`, `workflows`).
  * Real-time task execution records and error-catcher details.
  * Expander lists showing forensically caught tracebacks from the dead-letter queue (DLQ).
  * Replay button triggers to re-queue failures eagerly.
* Setup typed endpoints services layers:
  * `src/services/resume.service.ts`
  * `src/services/job.service.ts`
  * `src/services/workflow.service.ts`

---

## Relevant Files

```plaintext
frontend/src/app/dashboard/resumes/page.tsx
frontend/src/app/dashboard/jobs/page.tsx
frontend/src/app/dashboard/workflows/page.tsx
frontend/src/services/resume.service.ts
frontend/src/services/job.service.ts
frontend/src/services/workflow.service.ts
```

---

## Current Status

**COMPLETED**: All features sub-views, API endpoints services, and modal/drawer panels have been fully designed, implemented, compiled, and statically built with Next.js Turbopack, satisfying all product and technical guidelines.
**NEXT**: Set up Phase 6 — DevOps & Production Scaling (monitoring Flower/Prometheus/Grafana, CI/CD pipelines, scaling boundaries).
