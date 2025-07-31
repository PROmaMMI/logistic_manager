from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Order, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.base_crud import CRUDService, DatabaseException
from sqlalchemy.exc import SQLAlchemyError

class OrderService(CRUDService[Order, OrderCreate, OrderUpdate]):
    def __init__(self):
        super().__init__(Order)

    async def get_orders_by_status(self, db: AsyncSession, status: OrderStatus, skip=0, limit=100):
        try:    
            result = await db.execute(select(Order).where(Order.status == status).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Database error in get_orders_by_status(): {e}")
        
    async def get_orders_by_client(self, db: AsyncSession, client_id, skip=0, limit=100):
        try:   
            result = await db.execute(select(Order).where(Order.client_id == client_id).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Database error in get_orders_by_client(): {e}")