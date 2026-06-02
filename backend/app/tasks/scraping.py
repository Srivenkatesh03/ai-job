import asyncio
import logging
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.scraping.scrape_jobs_task", max_retries=4)
def scrape_jobs_task(self, query: str, location: str) -> dict:
    """
    Executes a job scraping pipeline to aggregate jobs matching queries and locations.
    """
    logger.info(f"Starting job scraping task [{self.request.id}] for: '{query}' in '{location}'")

    async def _run():
        # Simulated job scraping pipeline
        await asyncio.sleep(2)
        
        # Simulating external page failure retry triggers
        if "fail" in query.lower():
            raise RuntimeError("Scraping target returned anti-bot block page")

        jobs = [
            {
                "title": f"Senior {query} Engineer",
                "company": "Enterprise Software LLC",
                "location": location,
                "description": f"Excellent opportunity for a skilled {query} Developer.",
            },
            {
                "title": f"Lead {query} Architect",
                "company": "Innovative Startups Inc",
                "location": location,
                "description": f"Looking for {query} expertise to lead technical vision.",
            }
        ]
        
        logger.info(f"Successfully scraped {len(jobs)} jobs for query: '{query}'")
        return {"status": "success", "jobs_count": len(jobs), "jobs": jobs}

    try:
        return asyncio.run(_run())
    except Exception as exc:
        # Exponential backoff: 10s, 20s, 40s, 80s
        countdown = 10 * (2 ** self.request.retries)
        logger.warning(
            f"Job scraping failed on attempt {self.request.retries + 1}. "
            f"Retrying in {countdown}s. Error: {exc}"
        )
        raise self.retry(exc=exc, countdown=countdown)
