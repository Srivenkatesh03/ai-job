# CHANGELOG.md

# Project Changelog

# v0.1.0 — Architecture Initialization

## Added

* AI architecture planning
* workflow architecture
* backend engineering guide
* Docker strategy
* deployment pipeline design
* queue architecture
* observability planning

---

# v0.2.0 — Backend Foundation

## Added

* FastAPI application setup
* environment configuration
* health endpoints

## Changed

* standardized folder structure
* improved dependency injection setup

---

# v0.3.0 — Authentication & AI Layer Integration

## Added

* central database models with async `User` schema
* secure password hashing using `passlib[bcrypt]`
* stateless JWT token services (access, refresh, rotation)
* Bearer authentication header extractors and RBAC check middleware
* standard success/error wrappers conforming to REST payloads
* abstract AI provider interfaces and direct HTTPX async wrappers
* Google Gemini 1.5 and local Ollama integrations
* dynamic error failover / fallback factory runner
* central YAML prompt registry file and template parser
* automatic text embedding fallbacks (Anthropic delegating to OpenAI)
* docker-compose setup and .env templates
* 17-test suite verifying auth and AI components via memory SQLite

## Pending

* Celery integration
* Alembic migrations
* frontend dashboard

---

# v0.4.0 — Workflow Engine & Queue System

## Added

* central async Redis connection pooling and client session manager dependency (`app/core/redis.py`)
* production-ready Celery initialization and configuration (`app/core/celery_app.py`)
* isolated domain-specific named queues (`ai_tasks`, `notifications`, `scraping`, `workflows`, `analytics`)
* dynamic routing rules separating execution pathways
* custom `BaseWorkflowTask` subclass automating dead-letter queue (DLQ) serialization on final failure
* domain background workers for AI, notifications, scraping, and coordinated pipelines (`app/tasks/`)
* multi-step workflow pipelines using Celery canvas chain coordination
* production-grade multi-stage Docker build pipeline configuration (`backend/Dockerfile`)
* isolated worker service configurations in `docker-compose.yml`
* comprehensive 8-test suite covering dynamic retries, DLQ routing, eagerly executed canvas chains, and async runners

## Changed

* expanded backend dependencies with `celery` and `redis` integrations

---

# v0.5.0 — Frontend Scaffold & Authentication UI

## Added

* initialized Next.js App Router project with TypeScript and Tailwind CSS v4 in the `frontend` folder
* constructed Zustand persistent session authentication store (`frontend/src/stores/authStore.ts`)
* implemented secure, rotating, typed API fetch client with automatic 401 token refresh (`frontend/src/lib/apiClient.ts`)
* configured central Auth services connecting to registration, login, and profile REST endpoints (`frontend/src/services/auth.service.ts`)
* designed premium glassmorphic authentication pages (`login` and `register` views) with floating glowing elements
* created secure dashboard shell layout, responsive mobile-collapsible sliding Sidebar, and top Header status bar
* built Overview Dashboard homepage displaying metrics cards, Celery queue execution logs, and manual action pipelines
* verified production bundle compilation through successfully completed Turbo Next.js build

---

# v0.6.0 — DevOps & Production Scaling (Phase 6 Complete)

## Added

* instrumented FastAPI backend with real-time Prometheus client telemetry middleware (`backend/app/main.py`) exposing request statistics and duration latency histograms on `/metrics`
* configured Prometheus log scraper (`docker/prometheus/prometheus.yml`) targeting backend port 8000
* created centralized Loki logging pipeline configuration (`docker/loki/loki-config.yml`) for robust container log aggregation
* designed Promtail log scraper agent config (`docker/promtail/promtail-config.yml`) mounting container paths to aggregate and forward Docker logs
* created Grafana datasource auto-provisioning configs (`docker/grafana/provisioning/datasources/datasources.yml`) registering Prometheus and Loki on boot
* created Grafana dashboard auto-provisioning mapping (`docker/grafana/provisioning/dashboards/dashboards.yml`)
* designed pre-built glassmorphic Observability Dashboard template JSON (`docker/grafana/provisioning/dashboards/dashboard.json`) rendering API requests count, p95 latencies, and real-time Loki logging streams
* integrated Flower celery task queue dashboard and full Observability suite (Prometheus, Loki, Promtail, Grafana) inside `docker-compose.yml`
* designed production-grade Kubernetes HorizontalPodAutoscaler (HPA) manifest (`kubernetes/hpa.yaml`) configuring horizontal auto-scaling thresholds under load
* verified backend telemetry compiling and passing 100% of the 25-test suite flawlessly
