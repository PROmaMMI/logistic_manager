from app.schemas.tariff_zone import TariffZoneRead, TariffZoneCreate, TariffZoneUpdate
from app.services.tariff_zone_service import TariffZoneService
from app.api.base_router import CRUDRouter
from app.db.models import TariffZone
tariff_zone_service = TariffZoneService()

class TariffZoneRouter(CRUDRouter[TariffZone, TariffZoneRead, TariffZoneCreate, TariffZoneUpdate, TariffZoneService]):
    def __init__(self):
        super().__init__(
            prefix="/tariff_zones",
            tags=["Tariff Zones"],
            service=tariff_zone_service,
            read_schema=TariffZoneRead,
            create_schema=TariffZoneCreate,
            update_schema=TariffZoneUpdate,
        )

router = TariffZoneRouter().router