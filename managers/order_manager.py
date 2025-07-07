from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from schemas.cart_schemas import Cart
from schemas.cart_line_item_schemas import CartLineItem
from schemas.order_schemas import OrderCreate, Order
from schemas.product_variant_schemas import ProductVariant
from schemas.product_schemas import Product
from schemas.order_info_schemas import OrderInfo
from schemas.order_items_schemas import OrderItem
from models.order_model import OrderModel
from models.order_item_model import OrderItemModel
from models.product_model import ProductModel
from models.product_variant_model import ProductVariantModel


class OrderManager:
    @staticmethod
    async def create_order_and_order_items_from_cart(
        order_data: OrderCreate,
        cart: Cart,
        cart_line_items: list[CartLineItem],
        db: AsyncSession,
    ):
        order = OrderModel(**order_data.model_dump(), user_id=cart.user_id)
        db.add(order)
        await db.commit()
        order_items = []
        for item in cart_line_items:
            pv_stmt = select(ProductVariantModel).where(
                ProductVariantModel.id == item.product_variant_id
            )
            pv_result = await db.execute(pv_stmt)
            product_variant_row = pv_result.scalars().first()
            if not product_variant_row:
                raise NoResultFound(
                    f"No product variant found with id {item.product_variant_id}!"
                )
            product_variant = ProductVariant.model_validate(product_variant_row)
            p_stmt = select(ProductModel).where(
                ProductModel.id == product_variant.product_id
            )
            p_result = await db.execute(p_stmt)
            product_row = p_result.scalars().first()
            if not product_row:
                raise NoResultFound(
                    f"No product found with id {product_variant.product_id}!"
                )
            product = Product.model_validate(product_row)

            order_item = OrderItemModel(
                order_id=order.id,
                product_id=product.id,
                product_variant_id=product_variant.id,
                name=product.name,
                image_name=product_variant.image_name,
                price=product_variant.price,
                quantity=item.quantity,
            )
            order_items.append(order_item)

        db.add_all(order_items)
        await db.commit()

        return Order.model_validate(order)
    
    @staticmethod
    async def get_order_info_by_order_id(
        order_id: str, db: AsyncSession
    ) -> OrderInfo:
        stmt = (
            select(OrderModel)
            .where(OrderModel.id == order_id)
        )
        result = await db.execute(stmt)
        order = result.scalars().first()
        if not order:
            raise NoResultFound(f"Order with id {order_id} not found.")
        
        order_items_stmt = (
            select(OrderItemModel)
            .where(OrderItemModel.order_id == order.id)
        )

        order_items_result = await db.execute(order_items_stmt)
        order_items_rows = order_items_result.scalars().all()

        order_items = []
        for item_row in order_items_rows:
            order_item = OrderItem.model_validate(item_row)
            order_items.append(order_item)
        
        return OrderInfo(order=order, order_items=order_items)

    @staticmethod
    async def get_orders_info_by_user_id(
        user_id: str, db: AsyncSession
    ) -> list[OrderInfo]:
        stmt = (
            select(OrderModel)
            .where(OrderModel.user_id == user_id)
        )
        result = await db.execute(stmt)
        orders_rows = result.scalars().all()

        orders_info = []
        for order_row in orders_rows:
            order_items_stmt = (
                select(OrderItemModel)
                .where(OrderItemModel.order_id == order_row.id)
            )
            order_items_result = await db.execute(order_items_stmt)
            order_items_rows = order_items_result.scalars().all()

            order_items = []
            for item_row in order_items_rows:
                order_item = OrderItem.model_validate(item_row)
                order_items.append(order_item)

            orders_info.append(OrderInfo(order=order_row, order_items=order_items))
        
        return orders_info
