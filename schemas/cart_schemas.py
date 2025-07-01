from uuid import UUID
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_serializer


class CartStatusEnum(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CHECKED_OUT = "checked_out"
    ORDERED = "ordered"


class CartBase(BaseModel):
    status: CartStatusEnum = CartStatusEnum.ACTIVE


class CartCreate(CartBase):
    user_id: str


class CartConfig(CartBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID, _info):
        return str(user_id)
    

class Cart(CartConfig):
    pass
