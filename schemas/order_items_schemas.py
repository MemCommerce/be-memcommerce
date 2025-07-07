from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class OrderItemBase(BaseModel):
    name: str
    image_name: str | None = None
    price: float
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    product_id: UUID
    product_variant_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
    
    @field_serializer("order_id")
    def serialize_order_id(self, order_id: UUID, _info):
        return str(order_id)
    
    @field_serializer("product_id")
    def serialize_product_id(self, product_id: UUID, _info):
        return str(product_id)
    
    @field_serializer("product_variant_id")
    def serialize_product_variant_id(self, product_variant_id: UUID, _info):
        return str(product_variant_id)
    

class OrderItemResponse(OrderItem):
    """
    Response model for order items.
    This model is used to return order item details in API responses.
    """
    image_url: str | None = None
