from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ReviewBase(BaseModel):
    rating: int
    title: str | None = None
    content: str | None = None

    sentiment: str | None = None
    tags: list[str] | None = None
    aspect_sentiment: dict[str, str] | None = None


class ReviewData(ReviewBase):
    product_variant_id: str
    order_item_id: str


class Review(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_variant_id: UUID
    order_item_id: UUID
    user_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("product_variant_id")
    def serialize_product_variant_id(self, product_variant_id: UUID, _info):
        return str(product_variant_id)

    @field_serializer("order_item_id")
    def serialize_order_item_id(self, order_item_id: UUID, _info):
        return str(order_item_id)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID, _info):
        return str(user_id)


class ReviewSentiment(BaseModel):
    sentiment: str
    tags: list[str]
    aspect_sentiment: dict[str, str] | None = None