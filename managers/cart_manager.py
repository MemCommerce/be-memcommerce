from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from schemas.cart_schemas import CartCreate, Cart, CartStatusEnum
from schemas.cart_line_item_schemas import CartLineItemCreate, CartLineItem
from models.cart_model import CartModel
from models.cart_line_item_model import CartLineItemModel
from models.product_variant_model import ProductVariantModel


class CartManager:
    @staticmethod
    async def insert_cart(cart_data: CartCreate, db: AsyncSession) -> Cart:
        """
        Insert a new cart into the database.
        """
        new_cart = CartModel(**cart_data.model_dump())
        db.add(new_cart)
        await db.commit()
        await db.refresh(new_cart)
        return Cart.model_validate(new_cart)

    @staticmethod
    async def insert_cart_line_item(
        line_item_data: CartLineItemCreate, db: AsyncSession
    ) -> CartLineItem:
        """
        Insert a new cart line item into the database.
        """
        image_name = await db.execute(
            select(ProductVariantModel.image_name).where(
                ProductVariantModel.id == line_item_data.product_variant_id
            )
        )
        image_name = image_name.scalars().first()

        new_line_item = CartLineItemModel(
            **line_item_data.model_dump(), image_name=image_name
        )
        db.add(new_line_item)
        await db.commit()
        await db.refresh(new_line_item)
        return CartLineItem.model_validate(new_line_item)

    @staticmethod
    async def select_active_cart_by_user_id(
        user_id: str, db: AsyncSession
    ) -> Cart | None:
        """
        Retrieve the active cart for a specific user.
        """
        result = await db.execute(
            select(CartModel).where(
                CartModel.user_id == user_id, CartModel.status == CartStatusEnum.ACTIVE
            )
        )
        cart = result.scalars().first()
        return Cart.model_validate(cart) if cart else None

    @staticmethod
    async def select_cart_line_items(
        cart_id: str, db: AsyncSession
    ) -> list[CartLineItem]:
        """
        Retrieve all line items for a specific cart.
        """
        result = await db.execute(
            select(CartLineItemModel).where(CartLineItemModel.cart_id == cart_id)
        )
        line_items = result.scalars().all()
        return [CartLineItem.model_validate(item) for item in line_items]

    @staticmethod
    async def delete_cart_line_item(line_item_id: str, db: AsyncSession) -> None:
        """
        Delete a cart line item by its ID.
        """
        await db.execute(
            delete(CartLineItemModel).where(CartLineItemModel.id == line_item_id)
        )
        await db.commit()

    @staticmethod
    async def delete_cart(cart_id: str, db: AsyncSession) -> None:
        """
        Delete a cart by its ID.
        """
        await db.execute(delete(CartModel).where(CartModel.id == cart_id))
        await db.commit()

    @staticmethod
    async def update_cart_status(
        cart_id: str, status: CartStatusEnum, db: AsyncSession
    ) -> Cart:
        """
        Update the status of a cart.
        """
        result = await db.execute(select(CartModel).where(CartModel.id == cart_id))
        cart = result.scalars().first()

        if not cart:
            raise ValueError("Cart not found")

        cart.status = status  # type: ignore[reportAttributeAccessIssue]
        await db.commit()
        await db.refresh(cart)

        return Cart.model_validate(cart)

    @staticmethod
    async def update_cart_line_item_quantity(
        line_item_id: str, quantity: int, db: AsyncSession
    ) -> CartLineItem:
        """
        Update the quantity of a cart line item.
        """
        result = await db.execute(
            select(CartLineItemModel).where(CartLineItemModel.id == line_item_id)
        )
        line_item = result.scalars().first()

        if not line_item:
            raise ValueError("Cart line item not found")

        line_item.quantity = quantity  # type: ignore[reportAttributeAccessIssue]
        await db.commit()
        await db.refresh(line_item)

        return CartLineItem.model_validate(line_item)

    @staticmethod
    async def select_cart_line_item_by_id(
        line_item_id: str, db: AsyncSession
    ) -> CartLineItem | None:
        """
        Retrieve a specific cart line item by its ID.
        """
        result = await db.execute(
            select(CartLineItemModel).where(CartLineItemModel.id == line_item_id)
        )
        line_item = result.scalars().first()
        return CartLineItem.model_validate(line_item) if line_item else None
