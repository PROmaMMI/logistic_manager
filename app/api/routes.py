from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.route import RouteRead, RouteCreate, RouteUpdate
from app.services.route_service import RouteService
from app.api.base_router import CRUDRouter
from app.db.database import get_db
from app.db.models import Route
route_service = RouteService()

class RouteRouter(CRUDRouter[Route, RouteRead, RouteCreate, RouteUpdate, RouteService]):
    def __init__(self):
        super().__init__(
            prefix="/routes",
            tags=["Routes"],
            service=route_service,
            read_schema=RouteRead,
            create_schema=RouteCreate,
            update_schema=RouteUpdate,
        )

        @self.router.get("/by-order/{order_id}", response_model=RouteRead)
        async def get_by_order_id(order_id: str, db: AsyncSession = Depends(get_db)):
            route = await self.service.get_by_order_id(db, order_id)
            if not route:
                raise HTTPException(status_code=404, detail="Route not found")
            return route

router = RouteRouter().router