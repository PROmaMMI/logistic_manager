from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import TariffZone
from uuid import UUID
from typing import List, Optional

class TariffZoneService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tariff_zone(self, **zone_data) -> TariffZone:
        zone = TariffZone(**zone_data)
        self.session.add(zone)
        await self.session.commit()
        await self.session.refresh(zone)
        return zone

    async def get_tariff_zone(self, zone_id: UUID) -> Optional[TariffZone]:
        result = await self.session.execute(select(TariffZone).where(TariffZone.id == zone_id))
        return result.scalar_one_or_none()

    async def list_tariff_zones(self, skip: int = 0, limit: int = 100) -> List[TariffZone]:
        result = await self.session.execute(select(TariffZone).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_tariff_zone(self, zone_id: UUID, **update_data) -> Optional[TariffZone]:
        zone = await self.get_tariff_zone(zone_id)
        if not zone:
            return None
        for key, value in update_data.items():
            setattr(zone, key, value)
        self.session.add(zone)
        await self.session.commit()
        await self.session.refresh(zone)
        return zone

    async def delete_tariff_zone(self, zone_id: UUID) -> bool:
        zone = await self.get_tariff_zone(zone_id)
        if not zone:
            return False
        await self.session.delete(zone)
        await self.session.commit()
        return True