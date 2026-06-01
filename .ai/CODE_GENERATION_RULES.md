# CODE_GENERATION_RULES.md

# AI Code Generation Rules

## Overview

This document defines the mandatory rules AI coding agents must follow while generating, refactoring, or modifying code for the platform.

These rules apply to:

* backend code
* frontend code
* infrastructure code
* AI integrations
* workflow systems
* database logic
* DevOps configuration

The goal is to ensure production-grade consistency and maintainability.

---

# Mandatory Context Loading

Before generating code, ALWAYS read:

```plaintext id="jlwm401"
PROJECT_CONTEXT.md
ARCHITECTURE.md
RULES.md
TASKS.md
```

If relevant, also read:

```plaintext id="jlwm402"
DATABASE_PLAN.md
API_SPEC.md
WORKFLOW_ENGINE.md
SECURITY_PLAN.md
DEVOPS_GUIDE.md
```

---

# Primary Engineering Philosophy

## Core Principles

* generate production-grade code only
* prioritize maintainability
* avoid shortcuts
* prefer modular architecture
* follow clean architecture
* keep services loosely coupled

---

# Backend Generation Rules

## Backend Standards

Use:

* FastAPI
* async-first architecture
* dependency injection
* service/repository pattern
* Pydantic validation

---

# Backend Folder Rules

```plaintext id="jlwm403"
api/
services/
repositories/
models/
schemas/
workers/
ai/
domain/
core/
```

---

# Backend Constraints

* routes must not contain business logic
* repositories must isolate database access
* services must contain orchestration logic
* AI providers must remain abstracted

---

# Frontend Generation Rules

## Frontend Standards

Use:

* Next.js
* TypeScript
* Tailwind CSS
* React Query
* Zustand

---

# Frontend Constraints

* keep components reusable
* avoid large components
* isolate API logic
* avoid business logic inside UI

---

# API Generation Rules

## API Standards

* use RESTful routes
* validate all inputs
* use consistent response schemas
* add proper error handling

---

# Response Format

```json id="jlwm404"
{
  "success": true,
  "message": "",
  "data": {}
}
```

---

# Error Format

```json id="jlwm405"
{
  "success": false,
  "error": {
    "code": "",
    "message": ""
  }
}
```

---

# Database Generation Rules

## Database Standards

* PostgreSQL only
* UUID primary keys
* timestamps required
* migrations via Alembic
* indexes on critical fields

---

# Query Rules

* avoid N+1 queries
* use async queries
* optimize joins
* paginate large datasets

---

# AI Integration Rules

## AI Architecture

AI providers must use abstraction layers.

Never directly couple logic to:

* OpenAI
* Claude
* Gemini
* Ollama

---

# AI Provider Structure

```plaintext id="jlwm406"
providers/
├── base_provider.py
├── openai_provider.py
├── anthropic_provider.py
├── gemini_provider.py
└── ollama_provider.py
```

---

# Prompt Rules

* prompts must be modular
* prompts must be reusable
* prompts must support structured output
* prompts must not be hardcoded inside services

---

# Workflow Generation Rules

## Workflow Standards

* workflows must be event-driven
* workflows must support retries
* workflows must be observable
* workflows must be idempotent

---

# Queue Rules

Use separate queues for:

```plaintext id="jlwm407"
ai_tasks
notifications
scraping
analytics
retries
```

---

# Logging Rules

## Logging Standards

All services must use structured logging.

Required fields:

```plaintext id="jlwm408"
request_id
workflow_id
service_name
timestamp
```

---

# Security Rules

## Security Constraints

* validate all inputs
* sanitize uploads
* never hardcode secrets
* use parameterized queries
* secure all webhook endpoints

---

# Authentication Rules

## Auth Standards

Use:

* JWT
* refresh tokens
* RBAC

---

# DevOps Generation Rules

## Infrastructure Standards

Use:

* Docker
* Docker Compose
* Terraform
* GitHub Actions

---

# Docker Rules

* multi-stage builds
* non-root containers
* lightweight images

---

# CI/CD Rules

Pipeline stages:

```plaintext id="jlwm409"
lint
test
build
scan
deploy
```

---

# Observability Rules

## Monitoring Standards

Every service must expose:

```plaintext id="jlwm410"
/health
/ready
/live
```

---

# Required Metrics

Track:

* request latency
* queue depth
* AI token usage
* workflow failures

---

# Code Structure Rules

## File Limits

| Item            | Limit     |
| --------------- | --------- |
| Backend File    | 400 lines |
| React Component | 250 lines |
| Function        | 60 lines  |

---

# Refactoring Rules

## Refactoring Standards

When refactoring:

* preserve functionality
* reduce coupling
* improve readability
* improve modularity
* avoid unnecessary rewrites

---

# Dependency Rules

## Dependency Constraints

* minimize dependencies
* avoid abandoned libraries
* pin versions
* scan vulnerabilities

---

# Testing Rules

## Backend Tests

Required:

* unit tests
* integration tests
* API tests

---

# Frontend Tests

Required:

* component tests
* form validation tests
* API interaction tests

---

# Documentation Rules

## Documentation Standards

Document:

* APIs
* workflows
* infrastructure
* environment variables
* deployment steps

---

# Performance Rules

## Performance Standards

* async-first processing
* avoid blocking operations
* cache expensive AI calls
* paginate queries

---

# Scalability Rules

## Scalability Standards

Support:

* horizontal scaling
* worker isolation
* queue separation
* provider failover

---

# Forbidden Practices

## Never Generate

* monolithic services
* hardcoded secrets
* giant files
* duplicate logic
* tightly coupled AI providers
* synchronous heavy operations

---

# Code Style Rules

## Python Standards

* snake_case
* type hints
* descriptive naming
* docstrings for important functions

---

# TypeScript Standards

* strict typing
* reusable interfaces
* avoid any type
* modular components

---

# AI Agent Workflow

## Recommended Generation Order

```plaintext id="jlwm411"
1. Database schemas
2. Pydantic schemas
3. Repository layer
4. Service layer
5. API routes
6. Workers
7. Frontend integration
```

---

# Pull Request Standards

## PR Rules

Every PR should include:

* summary
* affected modules
* testing notes
* migration notes
* security considerations

---

# Architecture Preservation Rules

## Important Constraints

The AI assistant must preserve:

* clean architecture
* service boundaries
* queue architecture
* provider abstraction
* workflow modularity

---

# AI Memory Rules

## Context Awareness

Before generating new code:

* search existing utilities
* reuse existing services
* avoid duplicate abstractions
* preserve existing patterns

---

# Final Objective

All generated code should resemble:

* enterprise SaaS systems
* scalable AI platforms
* production DevOps infrastructure

The final codebase must remain:

* modular
* scalable
* observable
* secure
* maintainable

