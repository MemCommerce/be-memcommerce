from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert
from sqlalchemy.exc import NoResultFound

from schemas.size_schemas import Size, SizeData
from models.size_model import SizeModel


class SizeManager:
    @staticmethod
    async def insert_size(size_data: SizeData, db: AsyncSession) -> Size:
        stmt = insert(SizeModel).values(**size_data.model_dump()).returning(SizeModel)
        result = await db.execute(stmt)
        await db.commit()
        row = result.fetchone()
        return Size.model_validate(row[0])

    @staticmethod
    async def select_all_sizes(db: AsyncSession) -> list[Size]:
        sizes = (await db.execute(select(SizeModel))).scalars().all()
        return [Size.model_validate(size) for size in sizes]

    @staticmethod
    async def delete_size_by_id(id: str, db: AsyncSession) -> None:
        stmt = delete(SizeModel).where(SizeModel.id == id)
        await db.execute(stmt)
        await db.commit()

    @staticmethod
    async def update_size(size_id: str, size_data: SizeData, db: AsyncSession) -> Size:
        statement = select(SizeModel).where(SizeModel.id == size_id)
        result = await db.execute(statement)
        size = result.scalar_one_or_none()
        
        if size is None:
            raise NoResultFound(f"Size with id {size_id} not found")
        
        for field, value in size_data.model_dump(exclude_unset=True).items():
            setattr(size, field, value)
        
        await db.commit()
        await db.refresh(size)
        
        return Size.model_validate(size)
