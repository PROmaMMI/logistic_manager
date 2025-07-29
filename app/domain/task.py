from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Task:
    id: UUID
    order_id: Optional[UUID]
    assigned_to: UUID
    status: TaskStatus
    deadline: datetime
    description: str
    category: str
    created_at: datetime