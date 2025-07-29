from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderBase(BaseModel):
    client_id: UUID
    created_by: UUID
    tariff_zone_id: UUID
    status: OrderStatus = OrderStatus.created
    from_address: str
    to_address: str
    price: float
    delivery_date: datetime | None = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    tariff_zone_id: UUID | None = None
    status: OrderStatus | None = None
    from_address: str | None = None
    to_address: str | None = None
    price: float | None = None
    delivery_date: datetime | None = None

class OrderRead(OrderBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True