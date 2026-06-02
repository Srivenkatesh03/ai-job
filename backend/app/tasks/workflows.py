import logging
from celery import chain
from app.core.celery_app import celery_app
from app.tasks.ai import optimize_resume_task
from app.tasks.notifications import send_email_task

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.workflows.email_delivery_after_optimization_task")
def email_delivery_after_optimization_task(optimized_text: str, recipient: str, subject: str) -> dict:
    """
    Bridge task in a Celery chain that receives the optimized output from the 
    AI optimization step and triggers the email delivery task.
    """
    logger.info(f"Delivering optimized resume to: '{recipient}'")
    body = f"Hello,\n\nHere is your optimized resume content:\n\n{optimized_text}\n\nBest regards,\nAI Job Platform Team"
    # Delegate synchronously to the underlying send_email task function logic
    return send_email_task(recipient, subject, body)


@celery_app.task(name="app.tasks.workflows.run_resume_optimization_pipeline")
def run_resume_optimization_pipeline(resume_text: str, target_role: str, user_email: str) -> str:
    """
    Orchestrates the resume optimization workflow:
    1. Run AI optimize_resume_task.
    2. Route result through email_delivery_after_optimization_task to email the user.
    """
    logger.info(f"Orchestrating resume optimization pipeline for: '{user_email}'")
    
    # Build Celery canvas chain
    workflow_chain = chain(
        optimize_resume_task.s(resume_text, target_role),
        email_delivery_after_optimization_task.s(user_email, f"Optimized Resume: {target_role}"),
    )
    
    result = workflow_chain.delay()
    return result.id
