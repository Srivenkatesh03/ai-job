# DATA_FLOW.md

# System Data Flow Architecture

## Overview

This document describes how data moves throughout the platform across:

* frontend
* backend APIs
* AI systems
* workflow engines
* queues
* databases
* external integrations

The goal is to maintain a clear understanding of system interactions, workflow boundaries, and processing lifecycles.

---

# Data Flow Goals

## Primary Objectives

* traceable workflows
* predictable processing
* modular interactions
* scalable orchestration
* observable execution
* secure data movement

---

# High-Level Data Flow

```plaintext id="jlwm901"
Frontend
    │
    ▼
API Gateway / FastAPI
    │
 ┌──┼──────────────┐
 ▼  ▼              ▼
DB Services   AI Services   Workflow Engine
 │               │               │
 ▼               ▼               ▼
PostgreSQL    AI Providers    Redis Queue
                                    │
                                    ▼
                              Celery Workers
```

---

# Core System Components

## Primary Data Systems

| Component    | Responsibility      |
| ------------ | ------------------- |
| Frontend     | User interaction    |
| FastAPI      | API orchestration   |
| PostgreSQL   | Persistent storage  |
| Redis        | Queue + cache       |
| Celery       | Async workers       |
| AI Providers | AI processing       |
| n8n          | External automation |

---

# Authentication Flow

## Login Flow

```plaintext id="jlwm902"
User Login Request
      ↓
FastAPI Auth Service
      ↓
Credential Validation
      ↓
JWT Generation
      ↓
Response to Frontend
```

---

# Token Validation Flow

```plaintext id="jlwm903"
Client Request
      ↓
JWT Middleware
      ↓
Token Validation
      ↓
RBAC Validation
      ↓
Route Access
```

---

# Resume Upload Flow

## Resume Processing Lifecycle

```plaintext id="jlwm904"
User Uploads Resume
      ↓
Frontend Form Submission
      ↓
FastAPI Upload Endpoint
      ↓
File Validation
      ↓
Object Storage Upload
      ↓
DB Metadata Storage
      ↓
Queue Event Trigger
      ↓
AI Resume Processing
```

---

# Resume AI Optimization Flow

## AI Resume Workflow

```plaintext id="jlwm905"
resume.uploaded Event
      ↓
Celery Worker
      ↓
Resume Parser
      ↓
Prompt Builder
      ↓
AI Provider
      ↓
Response Validator
      ↓
ATS Score Generator
      ↓
Store Results in DB
      ↓
Notification Trigger
```

---

# Job Discovery Flow

## Job Aggregation Pipeline

```plaintext id="jlwm906"
Scheduler Trigger
      ↓
Scraping Worker
      ↓
External APIs / Sources
      ↓
Job Data Parsing
      ↓
Deduplication
      ↓
DB Storage
      ↓
Semantic Matching
      ↓
Notification System
```

---

# AI Request Flow

## Standard AI Pipeline

```plaintext id="jlwm907"
Frontend Request
      ↓
FastAPI Endpoint
      ↓
Service Layer
      ↓
Prompt Builder
      ↓
Provider Factory
      ↓
AI Provider
      ↓
Validation Layer
      ↓
Structured Response
      ↓
DB Logging
```

---

# AI Provider Flow

## Multi-Provider Routing

```plaintext id="jlwm908"
AI Service
    │
 ┌──┼───────────────┐
 ▼  ▼               ▼
GPT Claude      Ollama
```

---

# Fallback Provider Flow

## Provider Failure Handling

```plaintext id="jlwm909"
Primary Provider Failure
      ↓
Retry Attempt
      ↓
Fallback Provider
      ↓
Validation
      ↓
Return Result
```

---

# Queue Workflow

## Queue Lifecycle

```plaintext id="jlwm910"
Event Trigger
      ↓
Redis Queue
      ↓
Celery Worker
      ↓
Task Execution
      ↓
Retry Logic
      ↓
Completion / Failure
```

---

# Notification Flow

## Notification Lifecycle

```plaintext id="jlwm911"
Workflow Completed
      ↓
Notification Event
      ↓
Notification Worker
      ↓
Email / Slack / Discord
      ↓
Delivery Tracking
```

---

# Workflow Engine Flow

## Workflow Orchestration

```plaintext id="jlwm912"
Workflow Trigger
      ↓
Workflow Dispatcher
      ↓
Task Planning
      ↓
Queue Distribution
      ↓
Worker Execution
      ↓
Result Aggregation
```

---

# n8n Integration Flow

## External Automation Flow

```plaintext id="jlwm913"
Backend Event
      ↓
Webhook Trigger
      ↓
n8n Workflow
      ↓
External Service Integration
      ↓
Result Callback
      ↓
Backend Update
```

---

# Database Data Flow

## PostgreSQL Responsibilities

Stores:

* users
* resumes
* jobs
* workflow runs
* AI logs
* notifications
* analytics

---

# Redis Data Flow

## Redis Responsibilities

Handles:

* queues
* caching
* distributed locks
* workflow coordination

---

# Object Storage Flow

## File Storage Lifecycle

```plaintext id="jlwm914"
File Upload
      ↓
Validation
      ↓
S3/Object Storage
      ↓
Metadata Stored in PostgreSQL
```

---

# AI Memory Flow

## Memory Retrieval Pipeline

```plaintext id="jlwm915"
User Context
      ↓
Embedding Generation
      ↓
Vector Search
      ↓
Relevant Context Retrieval
      ↓
Prompt Enrichment
```

---

# Analytics Data Flow

## Analytics Pipeline

```plaintext id="jlwm916"
Application Events
      ↓
Metrics Collection
      ↓
Aggregation Workers
      ↓
Analytics DB
      ↓
Dashboard Visualization
```

---

# Logging Flow

## Observability Pipeline

```plaintext id="jlwm917"
Application Logs
      ↓
Structured Logging
      ↓
Loki
      ↓
Grafana Dashboards
```

---

# Monitoring Flow

## Metrics Pipeline

```plaintext id="jlwm918"
Application Metrics
      ↓
Prometheus
      ↓
Grafana
      ↓
Alerting
```

---

# Security Validation Flow

## Request Security Pipeline

```plaintext id="jlwm919"
Incoming Request
      ↓
Authentication
      ↓
Authorization
      ↓
Input Validation
      ↓
Rate Limiting
      ↓
Business Logic
```

---

# Error Handling Flow

## Failure Recovery

```plaintext id="jlwm920"
Task Failure
      ↓
Retry Logic
      ↓
Fallback Logic
      ↓
Dead-Letter Queue
      ↓
Monitoring Alert
```

---

# AI Agent Flow

## Future Multi-Agent Workflow

```plaintext id="jlwm921"
Planner Agent
      ↓
Task Distribution
      ↓
Specialized Agents
      ↓
Validation Agent
      ↓
Final Response
```

---

# Data Retention Flow

## Retention Lifecycle

```plaintext id="jlwm922"
Active Data
      ↓
Archive Policy
      ↓
Cold Storage
      ↓
Deletion Policy
```

---

# Backup Flow

## Backup Lifecycle

```plaintext id="jlwm923"
Database Snapshot
      ↓
Encrypted Backup
      ↓
Object Storage
      ↓
Retention Policy
```

---

# CI/CD Deployment Flow

## Deployment Pipeline

```plaintext id="jlwm924"
Git Push
      ↓
GitHub Actions
      ↓
Tests
      ↓
Docker Build
      ↓
Deployment
      ↓
Health Checks
```

---

# Scalability Flow

## Horizontal Scaling Strategy

```plaintext id="jlwm925"
Increased Load
      ↓
Autoscaling Trigger
      ↓
Additional Workers
      ↓
Load Distribution
```

---

# Observability Requirements

## All Flows Must Support

* request tracing
* workflow tracing
* metrics collection
* centralized logging

---

# Security Requirements

## All Data Flows Must Enforce

* encryption in transit
* authorization validation
* audit logging
* secure secrets handling

---

# Engineering Constraints

## Mandatory Rules

* workflows must remain async
* queues must remain isolated
* APIs must remain stateless
* AI providers must remain abstracted

---

# Forbidden Architecture Patterns

* direct DB access from frontend
* synchronous heavy AI workflows
* tightly coupled services
* shared mutable workflow state

---

# Future Expansion

## Planned Improvements

* event sourcing
* streaming workflows
* distributed tracing
* agent memory orchestration
* real-time workflow visualization

---

# Final Data Flow Goal

The platform should resemble:

* enterprise AI systems
* scalable workflow platforms
* event-driven SaaS architectures

The system must remain:

* traceable
* modular
* scalable
* observable
* production-ready
