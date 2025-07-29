from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"

class TaskBase(BaseModel):
    order_id: UUID | None = None
    assigned_to: UUID
    status: TaskStatus = TaskStatus.open
    deadline: datetime | None = None
    description: str
    category: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    order_id: UUID | None = None
    assigned_to: UUID | None = None
    status: TaskStatus | None = None
    deadline: datetime | None = None
    description: str | None = None
    category: str | None = None

class TaskRead(TaskBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True