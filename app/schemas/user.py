from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    operator = "operator"
    courier = "courier"

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    role: UserRole | None = None
    password: str | None = None

class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True