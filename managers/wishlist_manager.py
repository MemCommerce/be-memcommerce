from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from schemas.wishlist_item_schemas import WishlistItemCreate, WishlistItem
from models.wishlist_item_model import WishlistItemModel
from models.product_variant_model import ProductVariantModel


class WishlistManager:
    @staticmethod
    async def insert_wishlist_item(
        item_data: WishlistItemCreate, db: AsyncSession
    ) -> WishlistItem:
        """Insert a new wishlist item into the database."""
        image_name = await db.execute(
            select(ProductVariantModel.image_name).where(
                ProductVariantModel.product_id == item_data.product_id
            )
        )
        image_name = image_name.scalars().first()

        new_item = WishlistItemModel(**item_data.model_dump(), image_name=image_name)
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
        return WishlistItem.model_validate(new_item)

    @staticmethod
    async def select_wishlist_items(
        user_id: str, db: AsyncSession
    ) -> list[WishlistItem]:
        """Retrieve all wishlist items for a specific user."""
        result = await db.execute(
            select(WishlistItemModel).where(WishlistItemModel.user_id == user_id)
        )
        items = result.scalars().all()
        return [WishlistItem.model_validate(item) for item in items]

    @staticmethod
    async def delete_wishlist_item(item_id: str, db: AsyncSession) -> None:
        """Delete a wishlist item by its ID."""
        await db.execute(
            delete(WishlistItemModel).where(WishlistItemModel.id == item_id)
        )
        await db.commit()

    @staticmethod
    async def select_wishlist_item_by_id(
        item_id: str, db: AsyncSession
    ) -> WishlistItem | None:
        """Retrieve a specific wishlist item by its ID."""
        result = await db.execute(
            select(WishlistItemModel).where(WishlistItemModel.id == item_id)
        )
        item = result.scalars().first()
        return WishlistItem.model_validate(item) if item else None
