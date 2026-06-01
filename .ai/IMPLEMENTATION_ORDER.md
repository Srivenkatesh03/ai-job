# IMPLEMENTATION_ORDER.md

# Build Order

## Phase 1 — Foundation

* Docker setup
* FastAPI setup
* PostgreSQL
* Redis
* Celery
* Environment config

---

## Phase 2 — Core Backend

* Authentication
* User system
* RBAC
* Health endpoints

---

## Phase 3 — AI Layer

* Provider abstraction
* OpenAI integration
* Claude integration
* Prompt system

---

## Phase 4 — Workflow Engine

* Queue system
* Workflow dispatcher
* Retry logic
* Event system

---

## Phase 5 — Frontend

* Next.js setup
* Auth UI
* Dashboard
* Workflow UI

---

## Phase 6 — Production

* Monitoring
* CI/CD
* Deployment
* Scaling
