from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    contact_person: str
    phone: str | None = None
    email: EmailStr | None = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None

class ClientRead(ClientBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True