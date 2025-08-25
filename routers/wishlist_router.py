from fastapi import APIRouter, status, Depends, HTTPException

from db import get_db
from auth.token import get_current_user_id
from storage.gcp_storage import generate_signed_url
from schemas.wishlist_item_schemas import (
    WishlistItemCreate,
    WishlistItemReq,
    WishlistItemResp,
)
from managers.wishlist_manager import WishlistManager


router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.post("/", response_model=WishlistItemResp, status_code=status.HTTP_201_CREATED)
async def post_wishlist_item(
    item_req: WishlistItemReq,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """Add a new item to the user's wishlist."""
    item_data = WishlistItemCreate(
        product_id=item_req.product_id,
        price=item_req.price,
        name=item_req.name,
        user_id=user_id,
    )

    wishlist_item = await WishlistManager.insert_wishlist_item(item_data, db)
    image_url = generate_signed_url(wishlist_item.image_name)
    response_data = WishlistItemResp(
        id=wishlist_item.id,
        user_id=wishlist_item.user_id,
        product_id=wishlist_item.product_id,
        price=wishlist_item.price,
        name=wishlist_item.name,
        image_url=image_url,
    )
    return response_data


@router.get("/", response_model=list[WishlistItemResp])
async def get_user_wishlist(
    user_id: str = Depends(get_current_user_id), db=Depends(get_db)
):
    """Retrieve all wishlist items for the user."""
    items = await WishlistManager.select_wishlist_items(user_id, db)
    response_items = []
    for item in items:
        image_url = generate_signed_url(item.image_name)
        response_items.append(
            WishlistItemResp(
                id=item.id,
                user_id=item.user_id,
                product_id=item.product_id,
                price=item.price,
                name=item.name,
                image_url=image_url,
            )
        )
    return response_items


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist_item(
    item_id: str, user_id: str = Depends(get_current_user_id), db=Depends(get_db)
):
    """Delete a wishlist item by its ID."""
    existing_item = await WishlistManager.select_wishlist_item_by_id(item_id, db)
    if not existing_item or str(existing_item.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Item not found or does not belong to the user",
        )

    await WishlistManager.delete_wishlist_item(item_id, db)
    return {"message": "Wishlist item deleted successfully"}
