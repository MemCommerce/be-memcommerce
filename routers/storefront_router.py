from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from managers.storefront_manager import StorefrontManager
from schemas.storefront_schemas import StorefrontData


router = APIRouter(prefix="/storefront")


@router.get("/all", response_model=StorefrontData)
async def get_hole_storefront(db: AsyncSession = Depends(get_db)):
    data = await StorefrontManager.select_hole_storefront_data(db)
    return data
