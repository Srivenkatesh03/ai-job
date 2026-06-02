import asyncio
import logging
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.notifications.send_email_task", max_retries=5)
def send_email_task(self, recipient: str, subject: str, body: str) -> dict:
    """
    Simulates sending an email notification to a user with bounded retries.
    """
    logger.info(f"Starting email delivery task [{self.request.id}] to: '{recipient}'")

    async def _run():
        # Simulated async SMTP email delivery
        await asyncio.sleep(1)
        
        # Simulating potential connection error for retry test coverage
        if "fail" in recipient.lower():
            raise ConnectionError("SMTP Connection refused")
            
        logger.info(f"Email successfully delivered to {recipient}")
        return {"status": "sent", "recipient": recipient, "subject": subject}

    try:
        return asyncio.run(_run())
    except Exception as exc:
        # Exponential backoff: 5s, 10s, 20s, 40s, 80s
        countdown = 5 * (2 ** self.request.retries)
        logger.warning(
            f"Email delivery failed on attempt {self.request.retries + 1}. "
            f"Retrying in {countdown}s. Error: {exc}"
        )
        raise self.retry(exc=exc, countdown=countdown)


@celery_app.task(bind=True, name="app.tasks.notifications.send_webhook_task", max_retries=6)
def send_webhook_task(self, target_url: str, event_type: str, payload: dict) -> dict:
    """
    Dispatches a signed webhook event notification to a client callback URL.
    """
    logger.info(f"Starting webhook dispatch task [{self.request.id}] to: '{target_url}'")

    async def _run():
        import httpx
        
        # Simulated or actual async POST request
        headers = {"Content-Type": "application/json", "X-Event-Type": event_type}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(target_url, json=payload, headers=headers, timeout=10.0)
            
            if response.status_code >= 400:
                raise httpx.HTTPStatusError(
                    f"Webhook target returned error code {response.status_code}",
                    request=response.request,
                    response=response,
                )
                
        logger.info(f"Webhook {event_type} successfully dispatched to {target_url}")
        return {"status": "success", "url": target_url, "code": response.status_code}

    try:
        return asyncio.run(_run())
    except Exception as exc:
        # Exponential backoff: 10s, 20s, 40s, 80s, 160s, 320s
        countdown = 10 * (2 ** self.request.retries)
        logger.warning(
            f"Webhook dispatch failed on attempt {self.request.retries + 1}. "
            f"Retrying in {countdown}s. Error: {exc}"
        )
        raise self.retry(exc=exc, countdown=countdown)
