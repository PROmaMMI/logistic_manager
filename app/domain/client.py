from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class Client:
    id: UUID
    name: str
    contact_person: str
    phone: str
    email: str
    created_at: datetime