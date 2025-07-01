from uuid import uuid4

from sqlalchemy import Column, UUID, String, TIMESTAMP, func

from db import Base


class CartModel(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(20), nullable=False, default="active")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
