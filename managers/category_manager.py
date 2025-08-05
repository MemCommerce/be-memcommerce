from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound

from schemas.category_schemas import CategoryData, Category
from models.category_model import CategoryModel


class CategoryManager:
    @staticmethod
    async def insert_category(
        category_data: CategoryData, db: AsyncSession
    ) -> Category:
        category = CategoryModel(**category_data.model_dump())
        db.add(category)
        await db.commit()
        return Category.model_validate(category)

    @staticmethod
    async def select_all_categories(db: AsyncSession) -> list[Category]:
        categories = (await db.execute(select(CategoryModel))).scalars().all()
        return [Category.model_validate(category) for category in categories]

    @staticmethod
    async def delete_category_by_id(category_id: str, db: AsyncSession) -> None:
        statement = delete(CategoryModel).where(CategoryModel.id == category_id)
        await db.execute(statement)
        await db.commit()

    @staticmethod
    async def update_category(category_id: str, category_data: CategoryData, db: AsyncSession) -> Category:
        statement = select(CategoryModel).where(CategoryModel.id == category_id)
        result = await db.execute(statement)
        category = result.scalar_one_or_none()
        
        if category is None:
            raise NoResultFound(f"Category with id {category_id} not found")
        
        for field, value in category_data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        
        await db.commit()
        await db.refresh(category)
        
        return Category.model_validate(category)
