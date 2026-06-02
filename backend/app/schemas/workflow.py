from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class WorkflowRunRead(BaseModel):
    id: str
    status: str
    task_name: str
    queue: str
    logs: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkflowCreate(BaseModel):
    task_name: str
    queue: Optional[str] = "workflows"
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None
