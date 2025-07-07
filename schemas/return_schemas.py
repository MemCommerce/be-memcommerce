from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ReturnBase(BaseModel):
    status: str
    reason: str
    order_id: str


class ReturnCreate(ReturnBase):
    pass


class Return(ReturnBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID, _info):
        return str(user_id)
