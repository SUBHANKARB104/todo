from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskToggle(BaseModel):
    completed: bool


class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int
