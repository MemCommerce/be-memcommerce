from uuid import uuid4

from sqlalchemy import Column, UUID, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class ClaimItemModel(Base):
    __tablename__ = "claim_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    claim_id = Column(
        UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False
    )
    order_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("order_items.id", ondelete="CASCADE"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)
    resolution = Column(String(30), nullable=True)
    refund_amount = Column(Numeric(10, 2), nullable=True)

    claim = relationship("ClaimModel", back_populates="items")
