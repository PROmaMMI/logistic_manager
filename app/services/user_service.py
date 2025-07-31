from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base_crud import CRUDService, DatabaseException, ConflictException, NotFoundException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(CRUDService[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    async def create(self, db: AsyncSession, obj_in: UserCreate):
        try:    
            hashed_password = pwd_context.hash(obj_in.password)
            db_obj = self.model(
                email=obj_in.email,
                name=obj_in.name,
                role=obj_in.role,
                hashed_password=hashed_password
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise ConflictException(f"Integrity error in create(): {e}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Database error in create(): {e}")
        
    async def get_by_email(self, db: AsyncSession, email: str):
        try:
            result = await db.execute(select(User).where(User.email == email))
            obj = result.scalar_one_or_none()
            if obj is None:
                raise NotFoundException(f"User with email={email} not found")
            return obj
        except SQLAlchemyError as e:
            raise DatabaseException(f"Database error in get_by_email(): {e}")
    

    async def get_multi_by_role(self, db: AsyncSession, role, skip=0, limit=100):
        try:    
            result = await db.execute(select(User).where(User.role == role).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Database error in get_multi_by_role(): {e}")
