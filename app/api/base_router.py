from typing import Type, Generic, TypeVar, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.database import get_db

ModelType = TypeVar("ModelType")
ReadSchemaType = TypeVar("ReadSchemaType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ServiceType = TypeVar("ServiceType")

class CRUDRouter(Generic[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType, ServiceType]):
    def __init__(
        self,
        *,
        prefix: str,
        tags: list,
        service: ServiceType,
        read_schema: Type[ReadSchemaType],
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
    ):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.service = service
        self.read_schema = read_schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=List[self.read_schema])
        async def list_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
            return await self.service.list(db, skip=skip, limit=limit)

        @self.router.get("/{item_id}", response_model=self.read_schema)
        async def get_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
            return await self.service.get(db, item_id)


        @self.router.post("/", response_model=self.read_schema, status_code=status.HTTP_201_CREATED)
        async def create_item(item_in: self.create_schema, db: AsyncSession = Depends(get_db)):
            return await self.service.create(db, item_in)

        @self.router.put("/{item_id}", response_model=self.read_schema)
        async def update_item(item_id: UUID, item_in: self.update_schema, db: AsyncSession = Depends(get_db)):
            item = await self.service.get(db, item_id)
            return await self.service.update(db, item, item_in)

        @self.router.delete("/{item_id}", response_model=self.read_schema)
        async def delete_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
            return await self.service.delete(db, item_id)