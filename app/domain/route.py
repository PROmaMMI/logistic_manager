from dataclasses import dataclass
from uuid import UUID
from typing import List, Dict

@dataclass(frozen=True)
class Route:
    id: UUID
    order_id: UUID
    waypoints: List[Dict] 
    distance_km: float
    estimated_time_min: int