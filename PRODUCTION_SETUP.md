# Production Setup & Integration Guide

This guide outlines the critical configuration changes, environment variables, credentials, and code integrations required to transition the **AI Job Automation Platform** from a local developer environment to a secure, enterprise-grade cloud production stack.

---

## 📋 Production Readiness Checklist

| Category | Component | Dependency | Required Action |
| :--- | :--- | :--- | :--- |
| **Security** | JWT Cryptography | `SECRET_KEY` | Generate a strong cryptographically secure random secret. |
| **AI Processing** | LLM APIs | OpenAI / Anthropic / Gemini | Populate actual billing API keys for LLM query execution. |
| **Notifications** | Email Sender | SMTP / Transaction API | Replace simulated task with `aiosmtplib` or transactional API client. |
| **Automation** | Canvas Hooks | n8n / Webhooks | Point callback targets to active workflow execution triggers. |
| **Data & Cache** | Persistence | PostgreSQL & Redis | Replace local docker volumes with AWS RDS & ElastiCache. |
| **Observability** | Dashboards | Grafana Admin | Change default `admin`/`admin` dashboard passwords. |

---

## 1. Asymmetric Cryptography & JWT Security (`SECRET_KEY`)

The FastAPI backend uses JSON Web Tokens (JWT) to secure user profiles and enforce Role-Based Access Control (RBAC). 

> [!WARNING]
> Keeping the default developer fallback key `"supersecretkeychangeinproduction1234567890"` in a live environment exposes the application to JWT forgery, allowing attackers to forge admin auth payloads.

### How to Generate a Secure Key:
Run the following Python one-liner in your terminal to generate a secure 256-bit cryptographically random key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### How to Apply:
Add the generated value to your production `.env` file or cloud secrets manager (AWS Secrets Manager / GCP Secret Manager):
```env
SECRET_KEY=your_generated_32_byte_hex_string
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 2. Production AI Provider Configurations

Populate your `.env` file with live keys to unlock LLM fallbacks, cover letter generation, and ATS relevance scoring:

```env
# AI API Keys
OPENAI_API_KEY=sk-proj-yourActualOpenAiKey...
CLAUDE_API_KEY=sk-ant-yourActualAnthropicKey...
GEMINI_API_KEY=AIzaSyYourActualGoogleGeminiKey...
```

### Model Failover Pipeline
The system incorporates an automated failover factory (`backend/app/ai/providers/provider_factory.py`). If your primary LLM throws a rate limit error (HTTP 429) or outage exception, the prompt is automatically routed to active fallback models to prevent workflow crashes.

---

## 3. Real-World Email Dispatch Integration

The platform currently simulates email delivery inside the background Celery queue (`backend/app/app/tasks/notifications.py`).

### Existing Developer Placeholder:
```python
# Simulated SMTP execution
await asyncio.sleep(1)
```

### Production Deployment Update:
To dispatch real emails to users, install **`aiosmtplib`** inside the backend container and update the task code to send real messages via your SMTP server (e.g. Mailgun, SendGrid, or AWS SES):

```python
import asyncio
import logging
from email.message import EmailMessage
import aiosmtplib
from app.core.celery_app import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="app.tasks.notifications.send_email_task", max_retries=5)
def send_email_task(self, recipient: str, subject: str, body: str) -> dict:
    """
    Delivers a real transactional email notification to a user using an async SMTP link.
    """
    logger.info(f"Initiating production email dispatch [{self.request.id}] to: '{recipient}'")

    async def _send():
        message = EmailMessage()
        message["From"] = settings.SMTP_FROM
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        # Connects, authenticates, and dispatches asynchronously
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
            timeout=10.0
        )
        return {"status": "sent", "recipient": recipient, "subject": subject}

    try:
        return asyncio.run(_send())
    except Exception as exc:
        # Exponential retries: 5s, 10s, 20s, 40s...
        countdown = 5 * (2 ** self.request.retries)
        logger.warning(f"Email delivery failed (attempt {self.request.retries + 1}). Retrying in {countdown}s: {exc}")
        raise self.retry(exc=exc, countdown=countdown)
```

---

## 4. Hooking in n8n Automation Canvases

The canvas workflow steps (`backend/app/tasks/workflows.py`) coordinate classification, data scraping, and webhook triggers.

> [!TIP]
> To orchestrate job search queries dynamically through web engines, you can connect your Celery webhook dispatcher directly to **n8n** or **Make** canvas triggers.

### Webhook Dispatch Task (`backend/app/tasks/notifications.py`):
The `send_webhook_task` is already preconfigured to dispatch signed async HTTP POST payloads using `httpx`. Replace standard target callback parameters with your live canvas trigger:
```env
# Point this to your active n8n Webhook trigger URL node
N8N_WORKFLOW_WEBHOOK_URL=https://n8n.yourdomain.com/webhook/active-workflow-id
```

---

## 5. Transitioning to Managed Cloud Databases & Cache

For scalable growth and high availability, swap out local Dockerized volumes for managed enterprise databases:

```plaintext
      ┌────────────────────────────────────────────────────────┐
      │                   FastAPI Backend                      │
      └──────┬──────────────────────────────────────────┬──────┘
             │                                          │
             ▼                                          ▼
   [ AWS RDS PostgreSQL ]                     [ AWS ElastiCache ]
   - Master + Read Replicas                   - Multi-AZ Redis Cluster
   - Encrypted Storage Volume                 - Persistent Broker / Cache
```

### PostgreSQL Update (`.env`):
Replace standard docker DNS endpoints with your secure **AWS RDS PostgreSQL** (running asyncpg driver):
```env
DATABASE_URL=postgresql+asyncpg://aws_db_user:aws_db_password@rds-instance-endpoint.rds.amazonaws.com:5432/ai_job
```

### Redis Update (`.env`):
Replace local redis broker with your high-speed **AWS ElastiCache** Redis cluster endpoint:
```env
REDIS_URL=redis://elasticache-redis-cluster-endpoint.cache.amazonaws.com:6379/0
```

---

## 6. Telemetry & Observability Hardening

* **Grafana Port Routing:** In your production/local compose stacks, Grafana is routed to host port **`3010`** to prevent port conflicts on **`3000`** with the Next.js frontend container.
* **Credentials:** Default login is `admin` with password `admin`. 

> [!IMPORTANT]
> Upon your very first login to `http://localhost:3010`, you **must** change the administrator password to secure access to system-wide Loki logs and API metrics diagrams.
