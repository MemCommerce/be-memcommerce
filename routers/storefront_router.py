from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from managers.storefront_manager import StorefrontManager
from schemas.storefront_schemas import (
    StorefrontData,
    StorefrontProduct,
    SFProductWithReviews,
)
from schemas.pagination_schemas import PaginationResponse


router = APIRouter(prefix="/storefront")


@router.get("/all", response_model=StorefrontData)
async def get_whole_storefront(db: AsyncSession = Depends(get_db)):
    data = await StorefrontManager.select_whole_storefront_data(db)
    return data


@router.get("/paginated", response_model=PaginationResponse[StorefrontProduct])
async def get_paginated_storefront(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: AsyncSession = Depends(get_db),
):
    offset = page - 1
    data = await StorefrontManager.select_paginated_storefront_data(limit, offset, db)
    return data


@router.get("/product/{product_id}", response_model=SFProductWithReviews)
async def get_storefront_product_by_id(
    product_id: str, db: AsyncSession = Depends(get_db)
):
    data = await StorefrontManager.select_storefront_product_by_id(product_id, db)
    return data
