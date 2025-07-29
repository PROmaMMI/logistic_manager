from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class TaskComment:
    id: UUID
    task_id: UUID
    author_id: UUID
    text: str
    created_at: datetime