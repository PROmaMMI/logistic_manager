from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import TaskComment
from app.schemas.task_comment import TaskCommentCreate, TaskCommentUpdate
from app.services.base_crud import CRUDService

class TaskCommentService(CRUDService[TaskComment, TaskCommentCreate, TaskCommentUpdate]):
    def __init__(self):
        super().__init__(TaskComment)

    async def get_by_task_id(self, db: AsyncSession, task_id, skip=0, limit=100):
        result = await db.execute(select(TaskComment).where(TaskComment.task_id == task_id).offset(skip).limit(limit))
        return result.scalars().all()