from uuid import uuid4

from sqlalchemy import Column, UUID, String, ForeignKey, Numeric, TIMESTAMP, func
from sqlalchemy.orm import relationship

from db import Base


class RefundModel(Base):
    __tablename__ = "refunds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="SET NULL"))
    order_id = Column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False, default="pending")
    reason = Column(String(255), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    claim = relationship("ClaimModel", back_populates="refunds")
