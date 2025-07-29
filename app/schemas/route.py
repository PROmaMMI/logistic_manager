from pydantic import BaseModel
from uuid import UUID

class RouteBase(BaseModel):
    order_id: UUID
    waypoints: list[str] | None = None
    distance_km: float | None = None
    estimated_time_min: int | None = None

class RouteCreate(RouteBase):
    pass

class RouteUpdate(BaseModel):
    waypoints: list[str] | None = None
    distance_km: float | None = None
    estimated_time_min: int | None = None

class RouteRead(RouteBase):
    id: UUID

    class Config:
        orm_mode = True