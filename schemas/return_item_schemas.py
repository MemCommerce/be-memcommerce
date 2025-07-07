from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ReturnItemBase(BaseModel):
    quantity: int
    reason: str | None = None


class ReturnItemCreate(ReturnItemBase):
    order_item_id: str


class ReturnItem(ReturnItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    return_id: UUID
    order_item_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("return_id")
    def serialize_return_id(self, return_id: UUID, _info):
        return str(return_id)

    @field_serializer("order_item_id")
    def serialize_order_item_id(self, order_item_id: UUID, _info):
        return str(order_item_id)
