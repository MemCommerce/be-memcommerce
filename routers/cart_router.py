from fastapi import APIRouter, status, Depends, HTTPException

from db import get_db
from auth.token import get_current_user_id
from storage.gcp_storage import generate_signed_url
from schemas.cart_schemas import Cart, CartCreate, CartStatusEnum
from schemas.cart_line_item_schemas import (
    CartLineItemCreate,
    CartLineItemResp,
    CartLineItemReq,
)
from managers.cart_manager import CartManager


router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/", response_model=Cart, status_code=status.HTTP_201_CREATED)
async def post_cart(
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """
    Create a new cart for the user.
    """
    cart_data = CartCreate(user_id=user_id)
    cart_data.user_id = user_id
    new_cart = await CartManager.insert_cart(cart_data, db)
    return new_cart


@router.get("/", response_model=Cart)
async def get_user_cart(
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """
    Retrieve the user's active cart.
    """
    user_cart = await CartManager.select_active_cart_by_user_id(user_id, db)
    if not user_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active cart found for the user",
        )
    return user_cart


@router.post(
    "/add/cart_line_item",
    response_model=CartLineItemResp,
    status_code=status.HTTP_201_CREATED,
)
async def post_cart_line_item(
    cart_line_item_req: CartLineItemReq,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """
    Add a new cart line item to the user's cart.
    """
    user_cart = await CartManager.select_active_cart_by_user_id(user_id, db)
    if not user_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active cart found for the user",
        )

    cart_line_item_data = CartLineItemCreate(
        product_variant_id=cart_line_item_req.product_variant_id,
        quantity=cart_line_item_req.quantity,
        price=cart_line_item_req.price,
        name=cart_line_item_req.name,
        cart_id=str(user_cart.id),
    )

    cart_line_item = await CartManager.insert_cart_line_item(cart_line_item_data, db)
    image_url = await generate_signed_url(cart_line_item.image_name)
    response_data = CartLineItemResp(
        id=cart_line_item.id,
        cart_id=cart_line_item.cart_id,
        product_variant_id=cart_line_item.product_variant_id,
        quantity=cart_line_item.quantity,
        price=cart_line_item.price,
        name=cart_line_item.name,
        image_url=image_url,
    )
    return response_data


@router.delete("/cart_line_item/{line_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_line_item(
    line_item_id: str, user_id: str = Depends(get_current_user_id), db=Depends(get_db)
):
    """
    Delete a cart line item by its ID.
    """
    user_cart = await CartManager.select_active_cart_by_user_id(user_id, db)
    if not user_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active cart found for the user",
        )
    existing_line_item = await CartManager.select_cart_line_item_by_id(line_item_id, db)
    if not existing_line_item or existing_line_item.cart_id != user_cart.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Line item not found or does not belong to the user's active cart",
        )

    await CartManager.delete_cart_line_item(line_item_id, db)
    return {"message": "Cart line item deleted successfully"}


@router.patch(
    "/cart_line_item/{line_item_id}/{quantity}", response_model=CartLineItemResp
)
async def patch_cart_line_item_quantity(
    line_item_id: str,
    quantity: int,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """
    Update the quantity of a cart line item.
    """
    user_cart = await CartManager.select_active_cart_by_user_id(user_id, db)
    if not user_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active cart found for the user",
        )
    existing_line_item = await CartManager.select_cart_line_item_by_id(line_item_id, db)
    if not existing_line_item or existing_line_item.cart_id != user_cart.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Line item not found or does not belong to the user's active cart",
        )

    updated_line_item = await CartManager.update_cart_line_item_quantity(
        line_item_id, quantity, db
    )
    image_url = await generate_signed_url(updated_line_item.image_name)
    response_data = CartLineItemResp(
        id=updated_line_item.id,
        cart_id=updated_line_item.cart_id,
        product_variant_id=updated_line_item.product_variant_id,
        quantity=updated_line_item.quantity,
        price=updated_line_item.price,
        name=updated_line_item.name,
        image_url=image_url,
    )
    return response_data


@router.patch("/{cart_status}", response_model=Cart)
async def patch_cart_status(
    cart_status: CartStatusEnum,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """
    Update the status of a cart.
    """
    user_cart = await CartManager.select_active_cart_by_user_id(user_id, db)
    if not user_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active cart found for the user",
        )

    updated_cart = await CartManager.update_cart_status(
        str(user_cart.id), cart_status, db
    )
    return updated_cart
