from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ResumeBase(BaseModel):
    name: str
    upload_status: str


class ResumeCreate(ResumeBase):
    content: str


class ResumeRead(ResumeBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OptimizeRequest(BaseModel):
    resume_id: str
    target_role: str


class OptimizeResponse(BaseModel):
    optimized_resume: str
    ats_score: int
    suggestions: List[str]
