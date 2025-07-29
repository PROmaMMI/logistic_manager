from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class TariffZone:
    id: UUID
    name: str
    description: str
    tariff_params: dict