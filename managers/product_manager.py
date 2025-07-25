from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from schemas.product_schemas import ProductData, Product
from models.product_model import ProductModel


class ProductManager:
    @staticmethod
    async def insert_product(product_data: ProductData, db: AsyncSession) -> Product:
        product = ProductModel(**product_data.model_dump())
        db.add(product)
        await db.commit()
        return Product.model_validate(product)

    @staticmethod
    async def select_all_products(db: AsyncSession) -> list[Product]:
        products = (await db.execute(select(ProductModel))).scalars().all()
        return [Product.model_validate(product) for product in products]

    @staticmethod
    async def delete_product_by_id(id: str, db: AsyncSession) -> None:
        stmt = delete(ProductModel).where(ProductModel.id == id)
        await db.execute(stmt)
        await db.commit()

    @staticmethod
    async def update_product(product: Product, db: AsyncSession) -> Product:
        product_data = product.model_dump()
        updated_product = ProductModel(**product_data)

        merged_product = await db.merge(updated_product)
        await db.commit()
        await db.refresh(merged_product)

        return Product.model_validate(merged_product)
