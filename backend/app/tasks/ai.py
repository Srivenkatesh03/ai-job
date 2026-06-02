import asyncio
import logging
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.ai.optimize_resume_task", max_retries=3)
def optimize_resume_task(self, resume_text: str, target_role: str) -> str:
    """
    Optimizes a resume's bullet points and content based on a target role description.
    Uses the AI provider dynamic fallback factory to ensure delivery.
    """
    logger.info(f"Starting resume optimization task [{self.request.id}] for role: '{target_role}'")
    
    async def _run():
        from app.ai.prompt_manager import prompt_manager
        from app.ai.providers.provider_factory import ai_factory

        # Render prompts from the central template registry
        system_prompt = prompt_manager.render_prompt("resume_optimization", "system")
        user_prompt = prompt_manager.render_prompt(
            "resume_optimization",
            "user",
            resume_text=resume_text,
            target_role=target_role,
        )

        # Generate output using standard fallback orchestrator
        response = await ai_factory.generate_with_fallback(
            prompt=user_prompt,
            system_prompt=system_prompt,
            primary_provider="openai",
            fallback_providers=["anthropic", "gemini", "ollama"],
        )
        return response.content

    try:
        return asyncio.run(_run())
    except Exception as exc:
        # Exponential backoff: 5s, 15s, 45s
        countdown = 5 * (3 ** self.request.retries)
        logger.warning(
            f"AI optimization failed on attempt {self.request.retries + 1}. "
            f"Retrying in {countdown}s. Error: {exc}"
        )
        raise self.retry(exc=exc, countdown=countdown)


@celery_app.task(bind=True, name="app.tasks.ai.compute_job_relevance_task", max_retries=3)
def compute_job_relevance_task(self, job_title: str, job_description: str, resume_text: str) -> str:
    """
    Analyzes the relevance of a job description against a candidate's resume,
    calculating a match score and identifying key skills/gaps.
    """
    logger.info(f"Starting job relevance computation task [{self.request.id}] for title: '{job_title}'")

    async def _run():
        from app.ai.prompt_manager import prompt_manager
        from app.ai.providers.provider_factory import ai_factory

        system_prompt = prompt_manager.render_prompt("job_relevance", "system")
        user_prompt = prompt_manager.render_prompt(
            "job_relevance",
            "user",
            job_title=job_title,
            job_description=job_description,
            resume_text=resume_text,
        )

        response = await ai_factory.generate_with_fallback(
            prompt=user_prompt,
            system_prompt=system_prompt,
            primary_provider="openai",
            fallback_providers=["anthropic", "gemini", "ollama"],
        )
        return response.content

    try:
        return asyncio.run(_run())
    except Exception as exc:
        countdown = 5 * (3 ** self.request.retries)
        logger.warning(
            f"Job relevance task failed on attempt {self.request.retries + 1}. "
            f"Retrying in {countdown}s. Error: {exc}"
        )
        raise self.retry(exc=exc, countdown=countdown)
