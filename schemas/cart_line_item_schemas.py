from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_serializer


class CartLineItemBase(BaseModel):
    quantity: int
    price: float
    name: str


class CartLineItemReq(CartLineItemBase):
    product_variant_id: str


class CartLineItemCreate(CartLineItemBase):
    product_variant_id: str
    cart_id: str


class CartLineItemConfig(CartLineItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    cart_id: UUID
    product_variant_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("cart_id")
    def serialize_cart_id(self, cart_id: UUID, _info):
        return str(cart_id)

    @field_serializer("product_variant_id")
    def serialize_product_variant_id(self, product_variant_id: UUID, _info):
        return str(product_variant_id)


class CartLineItem(CartLineItemConfig):
    image_name: Optional[str] = None


class CartLineItemResp(CartLineItemConfig):
    image_url: Optional[str] = None
