# API_SPEC.md

# API Specification

## Overview

The platform exposes REST APIs for:

* authentication
* resume management
* AI workflows
* job discovery
* workflow automation
* notifications
* analytics

All APIs must follow consistent REST standards, authentication policies, validation rules, and response formats.

---

# API Standards

## Base URL

```plaintext id="n45z5w"
/api/v1
```

---

# General API Rules

* Use RESTful conventions
* Use JSON request/response format
* Use proper HTTP status codes
* Validate all inputs
* Return structured responses
* Use pagination for large datasets

---

# Authentication

## Authentication Method

* JWT Access Token
* Refresh Token

---

# Authorization Header

```plaintext id="xjq3gr"
Authorization: Bearer <token>
```

---

# Standard Success Response

```json id="gvjlwm"
{
  "success": true,
  "message": "Request successful",
  "data": {}
}
```

---

# Standard Error Response

```json id="c4gxeh"
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": {}
  }
}
```

---

# HTTP Status Standards

| Status Code | Usage                 |
| ----------- | --------------------- |
| 200         | Success               |
| 201         | Resource created      |
| 400         | Validation error      |
| 401         | Unauthorized          |
| 403         | Forbidden             |
| 404         | Resource not found    |
| 409         | Conflict              |
| 429         | Rate limited          |
| 500         | Internal server error |

---

# Authentication APIs

# Register User

## Endpoint

```plaintext id="1mz8m8"
POST /auth/register
```

---

## Request Body

```json id="htbubq"
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

---

## Response

```json id="m60t7y"
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": "uuid"
  }
}
```

---

# Login

## Endpoint

```plaintext id="y7e7nh"
POST /auth/login
```

---

## Request

```json id="yqkjlwm"
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

---

## Response

```json id="1q6w7t"
{
  "success": true,
  "data": {
    "access_token": "",
    "refresh_token": "",
    "expires_in": 3600
  }
}
```

---

# Refresh Token

## Endpoint

```plaintext id="zw04i9"
POST /auth/refresh
```

---

# Logout

## Endpoint

```plaintext id="jlwmvv"
POST /auth/logout
```

---

# Resume APIs

# Upload Resume

## Endpoint

```plaintext id="56ycn8"
POST /resumes/upload
```

---

## Content Type

```plaintext id="1d8g5r"
multipart/form-data
```

---

## Request Fields

| Field       | Type     |
| ----------- | -------- |
| file        | PDF/DOCX |
| resume_name | String   |

---

## Response

```json id="5zgjna"
{
  "success": true,
  "data": {
    "resume_id": "uuid",
    "upload_status": "completed"
  }
}
```

---

# Get User Resumes

## Endpoint

```plaintext id="3d8tcu"
GET /resumes
```

---

# Get Resume Details

## Endpoint

```plaintext id="0i3e6x"
GET /resumes/{resume_id}
```

---

# Delete Resume

## Endpoint

```plaintext id="zuzw1j"
DELETE /resumes/{resume_id}
```

---

# AI APIs

# Optimize Resume

## Endpoint

```plaintext id="2ct5k5"
POST /ai/resume/optimize
```

---

## Request

```json id="bkvp7z"
{
  "resume_id": "uuid",
  "target_role": "DevOps Engineer"
}
```

---

## Response

```json id="sn4goe"
{
  "success": true,
  "data": {
    "optimized_resume": "",
    "ats_score": 92,
    "suggestions": []
  }
}
```

---

# Generate Cover Letter

## Endpoint

```plaintext id="6qqq04"
POST /ai/cover-letter/generate
```

---

# AI Job Matching

## Endpoint

```plaintext id="6d8yn4"
POST /ai/job-match
```

---

# AI Interview Preparation

## Endpoint

```plaintext id="0ih4fc"
POST /ai/interview/questions
```

---

# Job APIs

# Search Jobs

## Endpoint

```plaintext id="y1avsz"
GET /jobs/search
```

---

## Query Parameters

| Parameter  | Type    |
| ---------- | ------- |
| keyword    | String  |
| location   | String  |
| experience | String  |
| remote     | Boolean |

---

# Save Job

## Endpoint

```plaintext id="jrzr9m"
POST /jobs/save
```

---

# Get Saved Jobs

## Endpoint

```plaintext id="jlwmrs"
GET /jobs/saved
```

---

# Application APIs

# Create Job Application

## Endpoint

```plaintext id="d1sh8u"
POST /applications
```

---

# Update Application Status

## Endpoint

```plaintext id="edp4cc"
PATCH /applications/{application_id}
```

---

# Get Applications

## Endpoint

```plaintext id="ybsjlwm"
GET /applications
```

---

# Workflow APIs

# Create Workflow

## Endpoint

```plaintext id="mpm8mq"
POST /workflows
```

---

# Trigger Workflow

## Endpoint

```plaintext id="zjlwmh"
POST /workflows/{workflow_id}/run
```

---

# Get Workflow Status

## Endpoint

```plaintext id="87j1hm"
GET /workflows/{workflow_id}/status
```

---

# Notification APIs

# Get Notifications

## Endpoint

```plaintext id="9fjlwm"
GET /notifications
```

---

# Mark Notification Read

## Endpoint

```plaintext id="2kkj1j"
PATCH /notifications/{notification_id}
```

---

# Analytics APIs

# Dashboard Analytics

## Endpoint

```plaintext id="yn4fqq"
GET /analytics/dashboard
```

---

# AI Usage Metrics

## Endpoint

```plaintext id="y3ckjp"
GET /analytics/ai-usage
```

---

# Pagination Standards

## Query Parameters

```plaintext id="ol8yqv"
?page=1&limit=20
```

---

# Pagination Response

```json id="4q6b4m"
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

# Rate Limiting

## Rules

Sensitive endpoints must use rate limiting.

Examples:

| Endpoint      | Limit    |
| ------------- | -------- |
| Login         | 5/minute |
| AI Generation | 20/hour  |
| Resume Upload | 10/day   |

---

# File Upload Rules

## Allowed Formats

* PDF
* DOCX

---

## Maximum File Size

```plaintext id="7yqzwu"
10 MB
```

---

# Validation Rules

## Global Validation

* sanitize inputs
* validate schemas
* reject malformed JSON
* validate uploaded files
* prevent prompt injection

---

# Security Standards

## Security Requirements

* JWT validation
* request validation
* RBAC authorization
* secure file handling
* audit logging

---

# API Documentation Standards

## Documentation Tools

* OpenAPI
* Swagger UI

---

# API Versioning Rules

## Versioning Strategy

```plaintext id="1h4ygt"
/api/v1/
/api/v2/
```

Old versions must remain backward compatible whenever possible.

---

# Async API Strategy

## Async Operations

Long-running operations should return:

```json id="ncv4i7"
{
  "task_id": "uuid",
  "status": "queued"
}
```

---

# Webhook Architecture

## Planned Webhooks

```plaintext id="jlwmzz"
workflow.completed
resume.optimized
job.matched
application.submitted
```

---

# Internal Service Communication

## Internal APIs

Internal services should use:

* service tokens
* signed requests
* private network communication

---

# Error Handling Standards

## Error Logging

All API failures must log:

* request ID
* endpoint
* user ID
* error code
* timestamp

---

# Future API Expansion

## Planned APIs

* AI agent APIs
* browser automation APIs
* SaaS billing APIs
* team collaboration APIs
* plugin APIs

---

# Final API Goal

The API layer should resemble:

* enterprise SaaS APIs
* scalable AI platforms
* production-grade workflow systems

The APIs must remain:

* secure
* scalable
* maintainable
* versioned
* well-documented
