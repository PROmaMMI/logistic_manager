from app.db.models import TariffZone
from app.schemas.tariff_zone import TariffZoneCreate, TariffZoneUpdate
from app.services.base_crud import CRUDService

class TariffZoneService(CRUDService[TariffZone, TariffZoneCreate, TariffZoneUpdate]):
    def __init__(self):
        super().__init__(TariffZone)