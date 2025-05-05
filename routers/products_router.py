from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.product_schemas import ProductData, Product
from managers.product_manager import ProductManager


product_router = APIRouter(prefix="/products")


@product_router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def post_product(product_data: ProductData, db: AsyncSession = Depends(get_db)):
    product = await ProductManager.insert_product(product_data, db)
    return product
