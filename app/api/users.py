from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.api.base_router import CRUDRouter
from app.db.database import get_db
from app.db.models import User

user_service = UserService()

class UserRouter(CRUDRouter[User, UserRead, UserCreate, UserUpdate, UserService]):
    def __init__(self):
        super().__init__(
            prefix="/users",
            tags=["Users"],
            service=user_service,
            read_schema=UserRead,
            create_schema=UserCreate,
            update_schema=UserUpdate,
        )

        @self.router.get("/by-email/{email}", response_model=UserRead)
        async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
            return await self.service.get_by_email(db, email)

        @self.router.get("/", response_model=List[UserRead])
        async def list_users(
            skip: int = 0,
            limit: int = 100,
            role: Optional[str] = None,
            db: AsyncSession = Depends(get_db)
        ):
            if role:
                return await self.service.get_multi_by_role(db, role, skip=skip, limit=limit)
            return await self.service.list(db, skip=skip, limit=limit)

router = UserRouter().router