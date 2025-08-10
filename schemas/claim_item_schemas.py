from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ClaimItemBase(BaseModel):
    quantity: int
    resolution: str | None = None
    refund_amount: Decimal | None = None


class ClaimItemCreate(ClaimItemBase):
    order_item_id: str


class ClaimItem(ClaimItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim_id: UUID
    order_item_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("claim_id")
    def serialize_claim_id(self, claim_id: UUID, _info):
        return str(claim_id)

    @field_serializer("order_item_id")
    def serialize_order_item_id(self, order_item_id: UUID, _info):
        return str(order_item_id)
