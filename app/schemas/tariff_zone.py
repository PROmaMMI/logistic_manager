from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TariffZoneBase(BaseModel):
    name: str
    description: str | None = None
    tariff_params: dict | None = None

class TariffZoneCreate(TariffZoneBase):
    pass

class TariffZoneUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    tariff_params: dict | None = None

class TariffZoneRead(TariffZoneBase):
    id: UUID

    class Config:
        orm_mode = True