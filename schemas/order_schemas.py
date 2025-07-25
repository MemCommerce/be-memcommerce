from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer


class OrderBase(BaseModel):
    full_name: str
    email: EmailStr
    address: str
    city: str
    country: str
    status: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID, _info):
        return str(user_id)
