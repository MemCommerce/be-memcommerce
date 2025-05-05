from sqlalchemy.ext.asyncio import AsyncSession

from schemas.product_schemas import ProductData, Product
from models.product_model import ProductModel


class ProductManager:
    @staticmethod
    async def insert_product(product_data: ProductData, db: AsyncSession) -> Product:
        product = ProductModel(**product_data.model_dump())
        db.add(product)
        await db.commit()
        return Product.model_validate(product)
