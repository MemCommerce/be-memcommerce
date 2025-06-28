from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.product_schemas import ProductData, Product
from managers.product_manager import ProductManager


products_router = APIRouter(prefix="/products")


@products_router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def post_product(product_data: ProductData, db: AsyncSession = Depends(get_db)):
    product = await ProductManager.insert_product(product_data, db)
    return product


@products_router.get("/", response_model=list[Product])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    products = await ProductManager.select_all_products(db)
    return products


@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, db: AsyncSession = Depends(get_db)):
    await ProductManager.delete_product_by_id(product_id, db)
    return "OK"


@products_router.put("/")
async def put_product(product: Product, db: AsyncSession = Depends(get_db)):
    updated_product = await ProductManager.update_product(product, db)
    return updated_product
