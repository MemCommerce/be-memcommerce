from pydantic import BaseModel

from schemas.review_schemas import Review
from schemas.order_items_schemas import OrderItem


class OrderItemWithImage(OrderItem):
    """Order item data with an optional signed image URL."""
    image_url: str | None = None


class UserReviewResponse(BaseModel):
    """Response model containing an order item and its related review if any."""
    review: Review | None = None
    order_item: OrderItemWithImage
