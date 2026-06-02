from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: Optional[str] = None
    relevance_score: Optional[int] = None
    skills_matched: Optional[List[str]] = None
    skills_gaps: Optional[List[str]] = None


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    model_config = ConfigDict(from_attributes=True)


class JobSaveRequest(BaseModel):
    job_id: str
