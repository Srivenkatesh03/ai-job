# BACKEND_GUIDE.md

# Backend Engineering Guide

## Overview

The backend is the central orchestration layer of the platform.

It is responsible for:

* API orchestration
* AI integration
* workflow execution
* queue coordination
* authentication
* database operations
* observability
* event processing

The backend must remain scalable, modular, async-first, and production-ready.

---

# Backend Goals

## Primary Objectives

* clean architecture
* modular services
* async processing
* provider independence
* workflow orchestration
* observability
* fault tolerance

---

# Core Backend Stack

## Technologies

| Layer         | Technology |
| ------------- | ---------- |
| API Framework | FastAPI    |
| ORM           | SQLAlchemy |
| Validation    | Pydantic   |
| Queue         | Celery     |
| Cache         | Redis      |
| Database      | PostgreSQL |
| Migrations    | Alembic    |

---

# Backend Folder Structure

## Standard Structure

```plaintext id="jlwm1401"
backend/
└── app/
    ├── api/
    ├── services/
    ├── repositories/
    ├── domain/
    ├── ai/
    ├── workers/
    ├── workflows/
    ├── models/
    ├── schemas/
    ├── db/
    ├── core/
    └── utils/
```

---

# Architecture Principles

## Core Principles

* separation of concerns
* dependency isolation
* async-first design
* modular services
* event-driven workflows

---

# API Layer Rules

## API Responsibilities

Routes should ONLY handle:

* request parsing
* validation
* authentication
* response formatting

---

# Forbidden API Patterns

Routes must NOT contain:

* business logic
* AI provider logic
* database queries
* workflow orchestration

---

# Service Layer

## Service Responsibilities

Services contain:

* business logic
* orchestration logic
* workflow coordination
* transaction management

---

# Repository Layer

## Repository Responsibilities

Repositories handle:

* database queries
* persistence logic
* query optimization

Repositories isolate the database from business logic.

---

# Domain Layer

## Domain Responsibilities

Contains:

* business entities
* workflow state rules
* core business logic

---

# AI Layer

## AI Responsibilities

Handles:

* provider abstraction
* prompt execution
* AI orchestration
* validation
* fallback logic

---

# Worker Layer

## Worker Responsibilities

Handles:

* background jobs
* async processing
* scheduled tasks
* retries

---

# Workflow Layer

## Workflow Responsibilities

Handles:

* event-driven execution
* workflow chaining
* orchestration logic

---

# API Structure

## Versioning

All APIs must use:

```plaintext id="jlwm1402"
/api/v1/
```

---

# Route Organization

## Example Structure

```plaintext id="jlwm1403"
api/v1/
├── auth.py
├── resumes.py
├── jobs.py
├── workflows.py
└── notifications.py
```

---

# Response Standards

## Success Response

```json id="jlwm1404"
{
  "success": true,
  "message": "",
  "data": {}
}
```

---

# Error Response

```json id="jlwm1405"
{
  "success": false,
  "error": {
    "code": "",
    "message": ""
  }
}
```

---

# Dependency Injection

## DI Rules

Use FastAPI dependency injection for:

* database sessions
* authentication
* repositories
* services

---

# Async Processing Rules

## Async Standards

Use async for:

* database operations
* API requests
* AI calls
* external integrations

---

# Database Standards

## Database Rules

* PostgreSQL only
* UUID primary keys
* timestamps required
* migrations via Alembic

---

# Model Structure

## Example Structure

```plaintext id="jlwm1406"
models/
├── user.py
├── resume.py
├── workflow.py
└── notification.py
```

---

# Schema Rules

## Pydantic Standards

Separate schemas for:

* request validation
* response serialization
* internal processing

---

# Schema Structure

```plaintext id="jlwm1407"
schemas/
├── auth.py
├── resume.py
├── workflow.py
└── notification.py
```

---

# AI Provider Architecture

## Provider Structure

```plaintext id="jlwm1408"
ai/providers/
├── base_provider.py
├── openai_provider.py
├── anthropic_provider.py
├── gemini_provider.py
└── ollama_provider.py
```

---

# AI Engineering Rules

## AI Constraints

* never hardcode prompts
* never tightly couple providers
* always validate outputs
* always support retries

---

# Queue Architecture

## Queue Categories

```plaintext id="jlwm1409"
ai_tasks
notifications
scraping
analytics
workflow_tasks
```

---

# Worker Structure

## Example Workers

```plaintext id="jlwm1410"
workers/
├── ai_worker.py
├── scraping_worker.py
├── notification_worker.py
└── analytics_worker.py
```

---

# Logging Standards

## Structured Logging

All services must log:

* request_id
* workflow_id
* service_name
* timestamps

---

# Security Rules

## Backend Security

* validate all inputs
* sanitize uploads
* use RBAC
* parameterized queries only

---

# File Upload Rules

## Resume Upload Constraints

Allowed formats:

* PDF
* DOCX

Maximum size:

```plaintext id="jlwm1411"
10 MB
```

---

# Error Handling Standards

## Backend Error Rules

* centralized exception handling
* structured errors
* retry support
* failure logging

---

# Observability Standards

## Health Endpoints

Every service must expose:

```plaintext id="jlwm1412"
/health
/ready
/live
```

---

# Monitoring Metrics

Track:

* API latency
* queue depth
* AI token usage
* workflow failures

---

# Caching Strategy

## Redis Usage

Use Redis for:

* queues
* caching
* rate limiting
* session management

---

# Authentication Rules

## Auth Standards

Use:

* JWT
* refresh tokens
* RBAC

---

# Environment Configuration

## Config Rules

Use centralized settings:

```plaintext id="jlwm1413"
core/config.py
```

---

# Environment Variables

## Required Variables

```plaintext id="jlwm1414"
DATABASE_URL
REDIS_URL
OPENAI_API_KEY
SECRET_KEY
```

---

# Testing Standards

## Backend Tests

Required:

* unit tests
* integration tests
* API tests
* worker tests

---

# Test Structure

```plaintext id="jlwm1415"
tests/
├── api/
├── services/
├── workers/
└── ai/
```

---

# Performance Rules

## Performance Constraints

* avoid blocking operations
* paginate queries
* cache expensive operations
* optimize DB access

---

# Scalability Rules

## Scalability Requirements

Support:

* horizontal scaling
* worker isolation
* provider failover
* distributed workflows

---

# Code Style Standards

## Python Rules

* snake_case
* type hints required
* descriptive naming
* modular functions

---

# File Size Rules

| Item     | Limit     |
| -------- | --------- |
| File     | 400 lines |
| Function | 60 lines  |
| Class    | 300 lines |

---

# Forbidden Practices

* business logic in routes
* hardcoded secrets
* synchronous heavy AI processing
* direct DB access from routes
* giant service files

---

# Future Backend Expansion

## Planned Features

* multi-agent orchestration
* event sourcing
* distributed tracing
* Kubernetes-native workers
* vector memory systems

---

# Final Backend Goal

The backend should resemble:

* enterprise SaaS backends
* AI orchestration systems
* scalable workflow platforms

The architecture must remain:

* modular
* scalable
* observable
* secure
* production-ready
