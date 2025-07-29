from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum

class OrderStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Order:
    id: UUID
    client_id: UUID
    created_by: UUID
    tariff_zone_id: UUID
    route_id: Optional[UUID]
    status: OrderStatus
    from_address: str
    to_address: str
    price: float
    created_at: datetime
    delivery_date: datetime