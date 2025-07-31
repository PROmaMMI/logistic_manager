from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import TaskComment
from app.schemas.task_comment import TaskCommentCreate, TaskCommentUpdate
from app.services.base_crud import CRUDService,  DatabaseException
from sqlalchemy.exc import SQLAlchemyError

class TaskCommentService(CRUDService[TaskComment, TaskCommentCreate, TaskCommentUpdate]):
    def __init__(self):
        super().__init__(TaskComment)

    async def get_by_task_id(self, db: AsyncSession, task_id, skip=0, limit=100):
        try:    
            result = await db.execute(select(TaskComment).where(TaskComment.task_id == task_id).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Database error in get_by_task_id(): {e}")