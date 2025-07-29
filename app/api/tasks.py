from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskRead, TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.api.base_router import CRUDRouter
from app.db.models import TaskStatus
from app.db.database import get_db
from app.db.models import Task
task_service = TaskService()

class TaskRouter(CRUDRouter[Task, TaskRead, TaskCreate, TaskUpdate, TaskService]):
    def __init__(self):
        super().__init__(
            prefix="/tasks",
            tags=["Tasks"],
            service=task_service,
            read_schema=TaskRead,
            create_schema=TaskCreate,
            update_schema=TaskUpdate,
        )

        @self.router.get("/by-user/{user_id}", response_model=List[TaskRead])
        async def get_tasks_by_user(
            user_id: str,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = Depends(get_db)
        ):
            return await self.service.get_tasks_by_user(db, user_id, skip=skip, limit=limit)

        @self.router.get("/by-status/{status}", response_model=List[TaskRead])
        async def get_tasks_by_status(
            status: TaskStatus,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = Depends(get_db)
        ):
            return await self.service.get_tasks_by_status(db, status, skip=skip, limit=limit)

router = TaskRouter().router