from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.db.models import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.base_crud import CRUDService, DatabaseException

class TaskService(CRUDService[Task, TaskCreate, TaskUpdate]):
    def __init__(self):
        super().__init__(Task)

    async def get_tasks_by_user(self, db: AsyncSession, user_id, skip=0, limit=100):
        try:    
            result = await db.execute(select(Task).where(Task.assigned_to == user_id).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
             raise DatabaseException(f"Database error in get_tasks_by_user(): {e}")

    async def get_tasks_by_status(self, db: AsyncSession, status: TaskStatus, skip=0, limit=100):
        try:    
            result = await db.execute(select(Task).where(Task.status == status).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Database error in get_tasks_by_status(): {e}")
