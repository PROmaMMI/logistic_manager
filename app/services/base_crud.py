from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class NotFoundException(Exception):
    pass

class DatabaseException(Exception):
    pass

class ConflictException(Exception):
    pass

class CRUDService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        try:    
            result = await db.execute(select(self.model).where(self.model.id == id))
            obj = result.scalar_one_or_none()
            if obj is None:
                raise NotFoundException(f'{self.model.__name__} ith id={id} not found')
            return obj
        except SQLAlchemyError as e:
            raise DatabaseException(f'Database error in get(): {e}')

    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        try:    
            result = await db.execute(select(self.model).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseException(f'Database error in list(): {e}')
        
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise ConflictException(f"Integrity error in create(): {e}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Database error in create(): {e}")

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise ConflictException(f"Integrity error in update(): {e}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Database error in update(): {e}")

    async def delete(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        try:   
            obj = await self.get(db, id)
            await db.delete(obj)
            await db.commit()
            return obj
        except NotFoundException:
            raise
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Database error in delete(): {e}")