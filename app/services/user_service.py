from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User
from uuid import UUID
from typing import List, Optional

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, **user_data) -> User:
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.session.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_user(self, user_id: UUID, **update_data) -> Optional[User]:
        user = await self.get_user(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: UUID) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True