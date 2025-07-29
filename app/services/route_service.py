from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Route
from uuid import UUID
from typing import List, Optional

class RouteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_route(self, **route_data) -> Route:
        route = Route(**route_data)
        self.session.add(route)
        await self.session.commit()
        await self.session.refresh(route)
        return route

    async def get_route(self, route_id: UUID) -> Optional[Route]:
        result = await self.session.execute(select(Route).where(Route.id == route_id))
        return result.scalar_one_or_none()

    async def get_route_by_order(self, order_id: UUID) -> Optional[Route]:
        result = await self.session.execute(select(Route).where(Route.order_id == order_id))
        return result.scalar_one_or_none()

    async def list_routes(self, skip: int = 0, limit: int = 100) -> List[Route]:
        result = await self.session.execute(select(Route).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_route(self, route_id: UUID, **update_data) -> Optional[Route]:
        route = await self.get_route(route_id)
        if not route:
            return None
        for key, value in update_data.items():
            setattr(route, key, value)
        self.session.add(route)
        await self.session.commit()
        await self.session.refresh(route)
        return route

    async def delete_route(self, route_id: UUID) -> bool:
        route = await self.get_route(route_id)
        if not route:
            return False
        await self.session.delete(route)
        await self.session.commit()
        return True