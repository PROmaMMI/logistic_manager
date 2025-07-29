from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Client
from uuid import UUID
from typing import List, Optional

class ClientService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_client(self, **client_data) -> Client:
        client = Client(**client_data)
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def get_client(self, client_id: UUID) -> Optional[Client]:
        result = await self.session.execute(select(Client).where(Client.id == client_id))
        return result.scalar_one_or_none()

    async def list_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        result = await self.session.execute(select(Client).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_client(self, client_id: UUID, **update_data) -> Optional[Client]:
        client = await self.get_client(client_id)
        if not client:
            return None
        for key, value in update_data.items():
            setattr(client, key, value)
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def delete_client(self, client_id: UUID) -> bool:
        client = await self.get_client(client_id)
        if not client:
            return False
        await self.session.delete(client)
        await self.session.commit()
        return True