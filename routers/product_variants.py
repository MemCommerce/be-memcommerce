from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.product_variant_schemas import ProductVariant, ProductVariantData
from managers.product_variant_manager import ProductVariantManager

router = APIRouter(prefix="/product-variants")


@router.post("/", response_model=ProductVariant, status_code=status.HTTP_201_CREATED)
async def post_product_variant(product_variant_data: ProductVariantData, db: AsyncSession = Depends(get_db)):
    product_variant = await ProductVariantManager.insert_product_variant(product_variant_data, db)
    return product_variant


@router.get("/", response_model=list[ProductVariant])
async def get_all_pv(db: AsyncSession = Depends(get_db)):
    product_variants = await ProductVariantManager.select_all_pv(db)
    return product_variants
