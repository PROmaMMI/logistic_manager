from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Route
from app.schemas.route import RouteCreate, RouteUpdate
from app.services.base_crud import CRUDService

class RouteService(CRUDService[Route, RouteCreate, RouteUpdate]):
    def __init__(self):
        super().__init__(Route)

    async def get_by_order_id(self, db: AsyncSession, order_id):
        result = await db.execute(select(Route).where(Route.order_id == order_id))
        return result.scalar_one_or_none()