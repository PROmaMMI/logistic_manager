from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    ADMIN = 'admin'
    OPERATOR = 'operator'
    COURIER = 'courier'

@dataclass(frozen=True)
class User:
    id: UUID
    email: str
    name: str
    role: UserRole
    hashed_password: str
    created_at: datetime