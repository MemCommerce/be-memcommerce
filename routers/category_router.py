from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.category_schemas import Category, CategoryData
from managers.category_manager import CategoryManager


category_router = APIRouter(prefix="/categories")


@category_router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def post_category(
    category_data: CategoryData, db: AsyncSession = Depends(get_db)
):
    category = await CategoryManager.insert_category(category_data, db)
    return category


@category_router.get("/")
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    categories = await CategoryManager.select_all_categories(db)
    return categories
