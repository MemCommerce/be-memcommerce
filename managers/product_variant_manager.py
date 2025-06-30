from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from models.product_variant_model import ProductVariantModel
from schemas.product_variant_schemas import ProductVariant, ProductVariantData


class ProductVariantManager:
    @staticmethod
    async def insert_product_variant(
        product_variant_data: ProductVariantData,
        image_name: Optional[str],
        db: AsyncSession,
    ) -> ProductVariant:
        product_variant = ProductVariantModel(
            **product_variant_data.model_dump(), image_name=image_name
        )
        db.add(product_variant)
        await db.commit()
        return ProductVariant.model_validate(product_variant)

    @staticmethod
    async def select_all_pv(db: AsyncSession) -> list[ProductVariant]:
        product_variants = (
            (await db.execute(select(ProductVariantModel))).scalars().all()
        )
        return [ProductVariant.model_validate(pv) for pv in product_variants]

    @staticmethod
    async def delete_product_variant(product_variant_id: str, db: AsyncSession) -> None:
        stmt = delete(ProductVariantModel).where(ProductVariantModel.id == product_variant_id)
        await db.execute(stmt)
        await db.commit()
