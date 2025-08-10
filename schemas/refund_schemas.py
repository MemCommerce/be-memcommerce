from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class RefundStatusEnum(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"


class RefundBase(BaseModel):
    amount: Decimal
    status: RefundStatusEnum = RefundStatusEnum.PENDING
    reason: str | None = None


class RefundCreate(RefundBase):
    order_id: str
    claim_id: str | None = None


class RefundStatusUpdate(BaseModel):
    status: RefundStatusEnum


class Refund(RefundBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    order_id: UUID
    claim_id: UUID | None = None

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID, _info):
        return str(user_id)

    @field_serializer("order_id")
    def serialize_order_id(self, order_id: UUID, _info):
        return str(order_id)

    @field_serializer("claim_id")
    def serialize_claim_id(self, claim_id: UUID | None, _info):
        return str(claim_id) if claim_id else None
