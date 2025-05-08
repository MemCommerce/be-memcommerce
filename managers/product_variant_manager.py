from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.product_variant_model import ProductVariantModel
from schemas.product_variant_schemas import ProductVariant, ProductVariantData


class ProductVariantManager:
    @staticmethod
    async def insert_product_variant(product_variant_data: ProductVariantData, db: AsyncSession) -> ProductVariant:
        product_variant = ProductVariantModel(**product_variant_data.model_dump())
        db.add(product_variant)
        await db.commit()
        return ProductVariant.model_validate(product_variant)

    @staticmethod
    async def select_all_pv(db: AsyncSession) -> list[ProductVariant]:
        product_variants = (await db.execute(select(ProductVariantModel))).scalars().all()
        return [ProductVariant.model_validate(pv) for pv in product_variants]
