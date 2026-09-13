from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Data accepted when creating a task."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: Literal["pending", "completed"] = "pending"
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    """Data accepted when updating a task."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: Literal["pending", "completed"] | None = None
    priority: Literal["low", "medium", "high"] | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    """Data returned by the task API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: Literal["pending", "completed"]
    priority: Literal["low", "medium", "high"]
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime


class TaskFromDescriptionRequest(BaseModel):
    """Natural-language description used to generate a task."""

    description: str = Field(min_length=1, max_length=5000)
