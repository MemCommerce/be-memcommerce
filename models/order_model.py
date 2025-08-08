from uuid import uuid4

from sqlalchemy import Column, UUID, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from db import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    status = Column(String(20), nullable=False, default="pending")

    # Shipping / contact info
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    line_items = relationship(
        "OrderItemModel", back_populates="order", cascade="all, delete-orphan"
    )
