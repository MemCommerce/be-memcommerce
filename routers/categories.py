from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from db import get_db
from schemas.category_schemas import Category, CategoryData
from managers.category_manager import CategoryManager


categories_router = APIRouter(prefix="/categories")


@categories_router.post(
    "/", response_model=Category, status_code=status.HTTP_201_CREATED
)
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


@categories_router.put("/{category_id}", response_model=Category)
async def put_category(
    category_id: str, category_data: CategoryData, db: AsyncSession = Depends(get_db)
):
    try:
        updated_category = await CategoryManager.update_category(
            category_id, category_data, db
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No category found with id {category_id}.",
        )

    return updated_category
