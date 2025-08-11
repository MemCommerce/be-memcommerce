from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_serializer


class WishlistItemBase(BaseModel):
    price: float
    name: str


class WishlistItemReq(WishlistItemBase):
    product_variant_id: str


class WishlistItemCreate(WishlistItemBase):
    product_variant_id: str
    user_id: str


class WishlistItemConfig(WishlistItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    product_variant_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID, _info):
        return str(user_id)

    @field_serializer("product_variant_id")
    def serialize_product_variant_id(self, product_variant_id: UUID, _info):
        return str(product_variant_id)


class WishlistItem(WishlistItemConfig):
    image_name: Optional[str] = None


class WishlistItemResp(WishlistItemConfig):
    image_url: Optional[str] = None
