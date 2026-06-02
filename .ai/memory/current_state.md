# CURRENT_STATE.md

# Current Project State

## Project

AI Job Automation Platform

---

# Current Progress

The project currently contains:

* Production-grade backend architecture
* central settings via `pydantic-settings`
* dialect-agnostic PostgreSQL/SQLite `User` database model
* JWT token creation, validation, and token rotation services
* Bearer header token validation dependencies and RBAC middleware
* REST endpoints for registration, login, refresh, profile, and admin screens
* structured, generic response/error schemas matching specifications
* abstract BaseProvider defining generation, streaming, and embeddings contracts
* direct HTTP integration wrappers for OpenAI, Claude, Gemini, and Ollama
* automatic model-to-model failover/fallback factory orchestrator
* central YAML-based Prompt Template Registry and parsing utilities
* central async Redis connection pooling and client session manager dependency
* production-ready Celery background worker setup with isolated domain queues
* custom BaseWorkflowTask automating dead-letter queue (DLQ) routing on final failure
* multi-step eager execution workflow pipeline using Celery canvas chain coordination
* production-grade multi-stage Docker build pipeline configuration
* comprehensive 25-test suite running standalone on async SQLite (incorporating eager Celery task execution)

---

# Current Backend Status

Phase 2 (Authentication & RBAC), Phase 3 (AI Layer Abstraction & Prompt Registry), and Phase 4 (Workflow Engine & Queue System) are completed and fully tested.

Current stack:

* FastAPI (async)
* SQLAlchemy (asyncpg)
* SQLite (aiosqlite for tests)
* python-jose (JWT)
* passlib / bcrypt (password hashing)
* httpx (direct async AI endpoint requests)
* PyYAML (prompt template management)
* Celery (asynchronous distributed workers)
* Redis (message broker and caching)

---

# Current Frontend Status

Base scaffold and authentication interface completed and fully compiled.

Current stack:

* Next.js App Router
* TypeScript
* Tailwind CSS v4
* Zustand (persistent store)
* Lucide React

---

# Current Infrastructure Status

Local database, cache dependencies, API backend, and isolated worker processes are standardized using docker-compose.

Implemented:

* docker-compose.yml (PostgreSQL 15, Redis 7, FastAPI Backend, 4 isolated Celery workers)
* .env environment variables template files
* backend/Dockerfile (production-ready multi-stage Python builder/runtime stages)

---

# Current Priority

Set up Phase 5 Feature Sub-Views (Resume Optimizer, Job Search, and Workflow Monitor panels).

---

# Immediate Next Tasks

1. Implement AI Resume Optimizer upload panel & STAR suggestion listing
2. Implement Job search aggregator layout with semantic matching displays
3. Implement Workflow monitoring panels with manual run/cancel triggers

---

# Important Constraints

* async-first architecture
* modular services
* provider-independent AI
* event-driven workflows
* production-ready structure

---

# Important Rules

* no business logic in routes
* no hardcoded secrets
* queues must remain isolated
* workflows must remain observable
