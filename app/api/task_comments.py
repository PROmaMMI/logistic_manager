from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task_comment import TaskCommentRead, TaskCommentCreate, TaskCommentUpdate
from app.services.task_comment_service import TaskCommentService
from app.api.base_router import CRUDRouter
from app.db.database import get_db
from app.db.models import TaskComment

task_comment_service = TaskCommentService()

class TaskCommentRouter(CRUDRouter[TaskComment, TaskCommentRead, TaskCommentCreate, TaskCommentUpdate, TaskCommentService]):
    def __init__(self):
        super().__init__(
            prefix="/task_comments",
            tags=["Task Comments"],
            service=task_comment_service,
            read_schema=TaskCommentRead,
            create_schema=TaskCommentCreate,
            update_schema=TaskCommentUpdate,
        )

        @self.router.get("/by-task/{task_id}", response_model=List[TaskCommentRead])
        async def get_by_task_id(
            task_id: str,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = Depends(get_db)
        ):
            return await self.service.get_by_task_id(db, task_id, skip=skip, limit=limit)

router = TaskCommentRouter().router