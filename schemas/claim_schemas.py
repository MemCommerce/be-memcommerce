from uuid import UUID
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_serializer


class ClaimStatusEnum(StrEnum):
    PENDING = "pending"
    REJECTED = "rejected"
    APPROVED_REFUND_PARTIAL = "approved_refund_partial"
    APPROVED_REFUND_FULL = "approved_refund_full"
    APPROVED_RETURN = "approved_return"
    APPROVED_REFUND_RETURN = "approved_refund_return"


class ClaimBase(BaseModel):
    status: ClaimStatusEnum = ClaimStatusEnum.PENDING
    reason: str | None = None


class ClaimCreate(ClaimBase):
    order_id: str


class ClaimStatusUpdate(BaseModel):
    status: ClaimStatusEnum


class Claim(ClaimBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    order_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID, _info):
        return str(user_id)

    @field_serializer("order_id")
    def serialize_order_id(self, order_id: UUID, _info):
        return str(order_id)
