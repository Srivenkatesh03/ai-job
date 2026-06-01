# RULES.md

# Global Engineering Rules

These rules apply to all generated code, workflows, infrastructure, APIs, AI integrations, database logic, and frontend components.

The AI assistant must strictly follow these rules during all code generation and refactoring tasks.

---

# Core Principles

* Prioritize maintainability over shortcuts
* Prefer explicit code over implicit behavior
* Keep services modular and loosely coupled
* Avoid monolithic business logic
* Write production-grade code only
* Follow clean architecture principles
* Use scalable async-first design patterns
* Avoid unnecessary dependencies

---

# Code Quality Standards

## General Rules

* Use descriptive variable names
* Avoid single-letter variables
* Keep functions focused on one responsibility
* Use type hints whenever possible
* Add docstrings to important functions
* Avoid duplicated logic
* Prefer composition over inheritance
* Avoid deeply nested conditionals

---

# File Size Limits

## Backend

* Maximum file size: 400 lines
* Maximum function size: 60 lines
* Maximum class size: 300 lines

## Frontend

* Maximum React component size: 250 lines
* Split reusable UI into separate components

---

# Folder Structure Rules

## Backend Structure

```plaintext
app/
├── api/
├── services/
├── ai/
├── workers/
├── db/
├── models/
├── schemas/
├── repositories/
├── domain/
└── core/
```

---

# Architecture Rules

## Separation of Concerns

* API layer handles HTTP only
* Services contain business logic
* Repositories handle database access
* AI modules handle model interactions
* Workers process background jobs
* Domain layer contains core business rules

---

# API Standards

## REST Standards

* Use RESTful naming conventions
* Use plural resource names
* Version all APIs
* Use consistent response formats

Example:

```json
{
  "success": true,
  "message": "Operation completed",
  "data": {}
}
```

---

# Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request"
  }
}
```

---

# Database Rules

## PostgreSQL Standards

* Use UUID primary keys
* Add timestamps to all tables
* Use migrations only
* Never modify production schema manually
* Add indexes for frequently queried columns
* Use foreign keys properly

---

# Naming Conventions

## Python

* snake_case for variables/functions
* PascalCase for classes
* UPPER_CASE for constants

## Frontend

* PascalCase for components
* camelCase for variables/functions

## Database

* snake_case table names
* snake_case column names

---

# AI Integration Rules

## AI Providers

* Never hardcode provider logic
* Use provider abstraction layer
* Support fallback providers
* Store prompts separately
* Log AI failures safely

---

# Prompt Engineering Rules

* Keep prompts modular
* Use reusable templates
* Avoid giant prompts
* Separate system prompts from user prompts
* Use structured output formats

---

# Security Rules

## Authentication

* Use JWT authentication
* Implement refresh tokens
* Hash passwords securely
* Never store plaintext credentials

---

## Secrets Management

* Never hardcode secrets
* Use environment variables
* Use secret managers in production

---

## Input Validation

* Validate all request inputs
* Sanitize uploaded files
* Validate file types
* Prevent SQL injection
* Prevent prompt injection

---

# Logging Rules

## Logging Standards

* Use structured logging
* Never log secrets
* Never log API keys
* Log request IDs
* Log workflow events

---

# Background Job Rules

## Queue Processing

* Jobs must be idempotent
* Add retry logic
* Add timeout handling
* Use dead-letter queues
* Log failures properly

---

# Frontend Standards

## UI Rules

* Use reusable components
* Keep business logic out of UI
* Use loading states
* Handle API errors gracefully
* Implement proper form validation

---

# State Management Rules

* Use centralized state management
* Avoid prop drilling
* Cache API responses when possible

---

# DevOps Rules

## Docker

* Use multi-stage builds
* Keep images lightweight
* Never run containers as root

---

## CI/CD

* Run linting before builds
* Run tests before deployment
* Block deployment on failures

---

# Testing Standards

## Backend Testing

* Unit tests required
* Integration tests required
* Mock external APIs
* Test error scenarios

---

## Frontend Testing

* Test critical components
* Test forms and validation
* Test loading/error states

---

# Documentation Rules

* Document APIs
* Document workflows
* Add README for important modules
* Keep architecture docs updated

---

# Git Rules

## Branch Naming

```plaintext
feature/
fix/
refactor/
hotfix/
```

---

# Commit Standards

Use meaningful commits.

Examples:

```plaintext
feat: add resume optimization workflow
fix: resolve queue retry bug
refactor: improve AI provider abstraction
```

---

# Performance Rules

* Use async endpoints where possible
* Avoid blocking operations
* Optimize database queries
* Cache expensive AI operations

---

# Scalability Rules

* Design services stateless
* Support horizontal scaling
* Avoid shared mutable state

---

# Forbidden Practices

* No hardcoded secrets
* No giant files
* No duplicated business logic
* No direct DB access from routes
* No AI provider lock-in
* No synchronous long-running tasks
* No unvalidated user inputs

---

# AI Code Generation Rules

Before generating code:

1. Read PROJECT_CONTEXT.md
2. Read ARCHITECTURE.md
3. Read RULES.md
4. Follow existing folder structure
5. Reuse existing utilities before creating new ones

---

# Engineering Philosophy

The project must resemble:

* enterprise SaaS architecture
* production-grade infrastructure
* scalable AI workflow systems
* modern DevOps platforms

All generated code should be suitable for:

* portfolio demonstration
* technical interviews
* production deployment
* long-term maintainability
