from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token import get_current_user_id
from db import get_db
from managers.cart_manager import CartManager
from managers.order_manager import OrderManager
from schemas.order_schemas import OrderCreate, Order


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def post_order(order_data: OrderCreate, user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    cart = await CartManager.select_active_cart_by_user_id(user_id, db)
    if not cart:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This user does not have active cart!")
    
    cart_line_items = await CartManager.select_cart_line_items(str(cart.id), db)
    if len(cart_line_items) == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User's cart does not have items!")
    
    order = await OrderManager.create_order_and_order_items_from_cart(order_data, cart, cart_line_items, db)
    return order
