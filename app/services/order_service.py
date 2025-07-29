from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from app.db import models
from app.db.models import Order
from uuid import UUID
from typing import List, Optional

class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_order(self, **order_data) -> Order:
        order = Order(**order_data)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
    
    async def get_order(self, order_id: UUID) -> Optional[Order]:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()


    async def list_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        result = await self.session.execute(select(Order).offset(skip).limit(limit))
        return result.scalars().all()       

    async def update_order(self, order_id: UUID, **update_data) -> Optional[Order]:
        order = await self.get_order(order_id)
        if not order:
            return None
        for key, value in update_data.items():
            setattr(order, key, value)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
    
    async def delete_order(self, order_id: UUID) -> bool:
        order = await self.get_order(order_id)
        if not order:
            return False
        await self.session.delete(order)
        await self.session.commit()
        return True