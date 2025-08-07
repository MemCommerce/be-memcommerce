from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from auth.token import get_current_user_id
from db import get_db
from storage.gcp_storage import generate_signed_url
from managers.cart_manager import CartManager
from managers.order_manager import OrderManager
from managers.review_manager import ReviewManager
from schemas.order_schemas import OrderCreate, Order
from schemas.order_items_schemas import OrderItemResponse
from schemas.order_info_schemas import OrderInfoResponse, OrderWithItems


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def post_order(
    order_data: OrderCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    cart = await CartManager.select_active_cart_by_user_id(user_id, db)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="This user does not have active cart!",
        )

    cart_line_items = await CartManager.select_cart_line_items(str(cart.id), db)
    if len(cart_line_items) == 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User's cart does not have items!",
        )

    order = await OrderManager.create_order_and_order_items_from_cart(
        order_data, cart, cart_line_items, db
    )
    await CartManager.complete_cart(str(cart.id), db)
    return order


@router.get("/", response_model=list[OrderWithItems], description="Admin route to get orders.")
async def get_orders(db: AsyncSession = Depends(get_db)):
    orders = await OrderManager.select_orders(db)
    return orders


@router.get("/order-info/{order_id}", response_model=OrderInfoResponse)
async def get_order_info(
    order_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        order_info = await OrderManager.get_order_info_by_order_id(order_id, db)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found.",
        )

    if str(order_info.order.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this order.",
        )

    response = OrderInfoResponse(
        order=order_info.order,
        order_items=[
            OrderItemResponse(
                id=item.id,
                name=item.name,
                image_name=item.image_name,
                price=item.price,
                quantity=item.quantity,
                order_id=item.order_id,
                product_id=item.product_id,
                product_variant_id=item.product_variant_id,
                image_url=generate_signed_url(item.image_name)
                if item.image_name
                else None,
            )
            for item in order_info.order_items
        ],
    )

    return response


@router.get("/user-orders", response_model=list[OrderInfoResponse])
async def get_user_orders(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    orders_info = await OrderManager.get_orders_info_by_user_id(user_id, db)

    response = [
        OrderInfoResponse(
            order=order_info.order,
            order_items=[
                OrderItemResponse(
                    id=item.id,
                    name=item.name,
                    image_name=item.image_name,
                    price=item.price,
                    quantity=item.quantity,
                    order_id=item.order_id,
                    product_id=item.product_id,
                    product_variant_id=item.product_variant_id,
                    review=await ReviewManager.select_review_by_order_item_id(str(item.id), db),
                    image_url=generate_signed_url(item.image_name)
                    if item.image_name
                    else None,
                )
                for item in order_info.order_items
            ],
        )
        for order_info in orders_info
    ]

    return response
