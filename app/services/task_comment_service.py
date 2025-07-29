from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import TaskComment
from uuid import UUID
from typing import List, Optional

class TaskCommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_comment(self, **comment_data) -> TaskComment:
        comment = TaskComment(**comment_data)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_comment(self, comment_id: UUID) -> Optional[TaskComment]:
        result = await self.session.execute(select(TaskComment).where(TaskComment.id == comment_id))
        return result.scalar_one_or_none()

    async def list_comments_by_task(self, task_id: UUID, skip: int = 0, limit: int = 100) -> List[TaskComment]:
        result = await self.session.execute(
            select(TaskComment).where(TaskComment.task_id == task_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update_comment(self, comment_id: UUID, **update_data) -> Optional[TaskComment]:
        comment = await self.get_comment(comment_id)
        if not comment:
            return None
        for key, value in update_data.items():
            setattr(comment, key, value)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def delete_comment(self, comment_id: UUID) -> bool:
        comment = await self.get_comment(comment_id)
        if not comment:
            return False
        await self.session.delete(comment)
        await self.session.commit()
        return True