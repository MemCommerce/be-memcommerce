from uuid import uuid4
from sqlalchemy import Column, UUID, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from db import Base


class ReturnModel(Base):
    __tablename__ = "returns"

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
        "ReturnItemModel", back_populates="return_request", cascade="all, delete-orphan"
    )
