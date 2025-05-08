from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.category_schemas import Category, CategoryData
from managers.category_manager import CategoryManager


categories_router = APIRouter(prefix="/categories")


@categories_router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def post_category(
    category_data: CategoryData, db: AsyncSession = Depends(get_db)
):
    category = await CategoryManager.insert_category(category_data, db)
    return category


@categories_router.get("/")
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    categories = await CategoryManager.select_all_categories(db)
    return categories


@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, db: AsyncSession = Depends(get_db)):
    await CategoryManager.delete_category_by_id(category_id, db)
    return "OK"
