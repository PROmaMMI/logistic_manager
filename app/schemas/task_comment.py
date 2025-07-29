from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TaskCommentBase(BaseModel):
    task_id: UUID
    author_id: UUID
    text: str

class TaskCommentCreate(TaskCommentBase):
    pass

class TaskCommentUpdate(BaseModel):
    text: str | None = None

class TaskCommentRead(TaskCommentBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True