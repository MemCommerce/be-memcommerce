from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from schemas.user_schemas import UserCreate, User
from models.user_model import UserModel


class UserManager:
    @staticmethod
    async def insert_user(user: UserCreate, db: AsyncSession) -> User:
        user = UserModel(**user.model_dump())
        db.add(user)
        await db.commit()
        return User.model_validate(user)

    @staticmethod
    async def select_user_by_email(email: str, db: AsyncSession) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
        return User.model_validate(user) if user else None

    @staticmethod
    async def select_user_by_id(user_id: str, db: AsyncSession) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise NoResultFound()
        
        return User.model_validate(user)
