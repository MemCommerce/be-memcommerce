from uuid import uuid4

from sqlalchemy import Column, UUID, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from db import Base


class ClaimModel(Base):
    __tablename__ = "claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    order_id = Column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)

    status = Column(String(30), nullable=False, default="pending")
    reason = Column(String(255), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    items = relationship(
        "ClaimItemModel", back_populates="claim", cascade="all, delete-orphan"
    )
    refunds = relationship(
        "RefundModel", back_populates="claim", cascade="all, delete-orphan"
    )
