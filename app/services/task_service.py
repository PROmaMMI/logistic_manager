from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from app.db import models
from app.db.models import Task
from uuid import UUID
from typing import List, Optional

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, **task_data) -> Task:
        task = Task(**task_data)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_task(self, task_id: UUID) -> Optional[Task]:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def list_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        result = await self.session.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_task(self, task_id: UUID, **update_data) -> Optional[Task]:
        task = await self.get_task(task_id)
        if not task:
            return None
        for key, value in update_data.items():
            setattr(task, key, value)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id: UUID) -> bool:
        task = await self.get_task(task_id)
        if not task:
            return False
        await self.session.delete(task)
        await self.session.commit()
        return True