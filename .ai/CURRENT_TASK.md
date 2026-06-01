# CURRENT_TASK.md

## Current Goal

Implement backend authentication system.

---

## Scope

ONLY implement:

* JWT auth
* login endpoint
* register endpoint
* refresh token endpoint
* RBAC middleware

---

## Relevant Files

```plaintext
backend/app/api/v1/auth.py
backend/app/services/auth_service.py
backend/app/models/user.py
backend/app/schemas/auth.py
```

---

## Constraints

* use FastAPI
* async-only
* PostgreSQL
* SQLAlchemy
* Pydantic v2
* JWT auth
* refresh tokens

---

## Do NOT

* implement frontend
* implement OAuth yet
* add unrelated features
* create giant files
