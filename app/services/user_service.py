from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base_crud import CRUDService

class UserService(CRUDService[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_multi_by_role(self, db: AsyncSession, role, skip=0, limit=100):
        result = await db.execute(select(User).where(User.role == role).offset(skip).limit(limit))
        return result.scalars().all()