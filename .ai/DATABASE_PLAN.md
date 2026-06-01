# DATABASE_PLAN.md

# Database Architecture Plan

## Overview

The platform uses PostgreSQL as the primary relational database.

The database is designed for:

* scalability
* maintainability
* auditability
* workflow tracking
* AI workflow orchestration
* analytics support
* event-driven processing

---

# Database Goals

## Primary Objectives

* normalized schema design
* strong relational integrity
* scalable indexing strategy
* audit logging support
* async-friendly operations
* AI workflow tracking
* efficient querying

---

# Primary Database

## Database Engine

* PostgreSQL

---

# Optional Extensions

## Recommended Extensions

* pgvector
* uuid-ossp
* pgcrypto

---

# Database Design Rules

## Global Standards

* Use UUID primary keys
* Add created_at timestamps
* Add updated_at timestamps
* Use soft deletion where needed
* Use indexed foreign keys
* Avoid storing unstructured AI blobs unnecessarily

---

# Naming Conventions

## Table Naming

* snake_case
* plural table names

Examples:

```plaintext id="0u90hj"
users
resumes
job_applications
workflow_runs
```

---

# Column Naming

* snake_case
* descriptive names
* avoid abbreviations

---

# Core Tables

# Users Table

## users

Purpose:

Stores platform user accounts.

---

## Columns

| Column        | Type      | Description        |
| ------------- | --------- | ------------------ |
| id            | UUID      | Primary key        |
| email         | VARCHAR   | Unique email       |
| password_hash | TEXT      | Hashed password    |
| full_name     | VARCHAR   | User full name     |
| role          | VARCHAR   | User role          |
| is_active     | BOOLEAN   | Active status      |
| created_at    | TIMESTAMP | Creation timestamp |
| updated_at    | TIMESTAMP | Update timestamp   |

---

# Resumes Table

## resumes

Purpose:

Stores uploaded resumes and metadata.

---

## Columns

| Column            | Type      |
| ----------------- | --------- |
| id                | UUID      |
| user_id           | UUID      |
| original_filename | VARCHAR   |
| storage_path      | TEXT      |
| parsed_text       | TEXT      |
| ats_score         | INTEGER   |
| created_at        | TIMESTAMP |

---

# Resume Analysis Table

## resume_analyses

Purpose:

Stores AI-generated resume analysis.

---

## Columns

| Column        | Type      |
| ------------- | --------- |
| id            | UUID      |
| resume_id     | UUID      |
| provider      | VARCHAR   |
| model         | VARCHAR   |
| analysis_json | JSONB     |
| token_usage   | INTEGER   |
| created_at    | TIMESTAMP |

---

# Jobs Table

## jobs

Purpose:

Stores aggregated job postings.

---

## Columns

| Column       | Type      |
| ------------ | --------- |
| id           | UUID      |
| source       | VARCHAR   |
| title        | VARCHAR   |
| company      | VARCHAR   |
| location     | VARCHAR   |
| description  | TEXT      |
| salary_range | VARCHAR   |
| external_url | TEXT      |
| created_at   | TIMESTAMP |

---

# Job Matches Table

## job_matches

Purpose:

Stores AI-generated resume-to-job matches.

---

## Columns

| Column          | Type      |
| --------------- | --------- |
| id              | UUID      |
| user_id         | UUID      |
| resume_id       | UUID      |
| job_id          | UUID      |
| relevance_score | FLOAT     |
| match_reason    | TEXT      |
| created_at      | TIMESTAMP |

---

# Applications Table

## job_applications

Purpose:

Tracks job applications.

---

## Columns

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| user_id    | UUID      |
| job_id     | UUID      |
| status     | VARCHAR   |
| applied_at | TIMESTAMP |
| notes      | TEXT      |

---

# Workflows Table

## workflows

Purpose:

Stores workflow definitions.

---

## Columns

| Column        | Type      |
| ------------- | --------- |
| id            | UUID      |
| name          | VARCHAR   |
| description   | TEXT      |
| workflow_type | VARCHAR   |
| is_active     | BOOLEAN   |
| created_at    | TIMESTAMP |

---

# Workflow Runs Table

## workflow_runs

Purpose:

Tracks workflow execution history.

---

## Columns

| Column       | Type      |
| ------------ | --------- |
| id           | UUID      |
| workflow_id  | UUID      |
| status       | VARCHAR   |
| started_at   | TIMESTAMP |
| completed_at | TIMESTAMP |
| logs         | JSONB     |

---

# AI Requests Table

## ai_requests

Purpose:

Tracks AI API requests and metadata.

---

## Columns

| Column            | Type      |
| ----------------- | --------- |
| id                | UUID      |
| provider          | VARCHAR   |
| model             | VARCHAR   |
| prompt_tokens     | INTEGER   |
| completion_tokens | INTEGER   |
| latency_ms        | INTEGER   |
| workflow_id       | UUID      |
| created_at        | TIMESTAMP |

---

# Notifications Table

## notifications

Purpose:

Stores user notifications.

---

## Columns

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| user_id    | UUID      |
| type       | VARCHAR   |
| message    | TEXT      |
| is_read    | BOOLEAN   |
| created_at | TIMESTAMP |

---

# Audit Logs Table

## audit_logs

Purpose:

Tracks important system actions.

---

## Columns

| Column       | Type      |
| ------------ | --------- |
| id           | UUID      |
| entity_type  | VARCHAR   |
| entity_id    | UUID      |
| action       | VARCHAR   |
| performed_by | UUID      |
| metadata     | JSONB     |
| created_at   | TIMESTAMP |

---

# Relationships

## Relationship Rules

```plaintext id="3onvt8"
users
 ├── resumes
 ├── job_applications
 ├── notifications
 └── workflow_runs

resumes
 ├── resume_analyses
 └── job_matches

jobs
 └── job_matches

workflows
 └── workflow_runs
```

---

# Indexing Strategy

## Required Indexes

### users

* email
* role

### resumes

* user_id
* created_at

### jobs

* title
* company
* location

### workflow_runs

* workflow_id
* status

### ai_requests

* provider
* created_at

---

# JSONB Usage Rules

## JSONB Should Be Used For

* AI outputs
* workflow metadata
* logs
* dynamic configuration

Avoid excessive JSONB usage for relational data.

---

# Soft Delete Strategy

## Soft Delete Columns

```plaintext id="siv7xj"
deleted_at
is_deleted
```

Used for:

* workflows
* resumes
* notifications

---

# Migration Strategy

## Migration Tool

* Alembic

---

# Migration Rules

* Never edit old migrations
* One feature per migration
* Always test rollback support
* Add indexes during migrations

---

# Query Optimization

## Performance Rules

* avoid N+1 queries
* use eager loading carefully
* paginate large datasets
* optimize AI analytics queries

---

# Security Rules

## Database Security

* least privilege access
* parameterized queries only
* encrypted credentials
* secure backups

---

# Backup Strategy

## Backup Rules

* daily backups
* point-in-time recovery
* encrypted backups
* automated retention cleanup

---

# Future Database Features

## Planned Expansion

* vector embeddings
* analytics warehouse
* event sourcing
* distributed workflows
* AI memory persistence

---

# Vector Database Strategy

## Future Semantic Search

Potential vector storage:

* pgvector
* Qdrant
* Pinecone

Use cases:

* resume similarity
* semantic job search
* AI memory retrieval
* recommendation systems

---

# Database Scaling Strategy

## Scaling Goals

* read replicas
* partitioning
* async workers
* caching layers
* optimized indexing

---

# Final Database Objective

The database architecture should support:

* enterprise-scale workflows
* AI orchestration systems
* large-scale job processing
* SaaS analytics
* production-grade reliability

The design must remain scalable, maintainable, and optimized for long-term growth.
