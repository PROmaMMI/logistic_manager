from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.order import OrderRead, OrderCreate, OrderUpdate
from app.services.order_service import OrderService
from app.api.base_router import CRUDRouter
from app.db.models import OrderStatus
from app.db.database import get_db
from app.db.models import Order
order_service = OrderService()

class OrderRouter(CRUDRouter[Order, OrderRead, OrderCreate, OrderUpdate, OrderService]):
    def __init__(self):
        super().__init__(
            prefix="/orders",
            tags=["Orders"],
            service=order_service,
            read_schema=OrderRead,
            create_schema=OrderCreate,
            update_schema=OrderUpdate,
        )

        @self.router.get("/by-status/{status}", response_model=List[OrderRead])
        async def get_orders_by_status(
            status: OrderStatus,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = Depends(get_db)
        ):
            return await self.service.get_orders_by_status(db, status, skip=skip, limit=limit)

        @self.router.get("/by-client/{client_id}", response_model=List[OrderRead])
        async def get_orders_by_client(
            client_id: str,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = Depends(get_db)
        ):
            return await self.service.get_orders_by_client(db, client_id, skip=skip, limit=limit)

router = OrderRouter().router