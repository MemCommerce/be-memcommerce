from uuid import uuid4

from sqlalchemy import Column, UUID, String, TIMESTAMP, func, Numeric, Integer

from db import Base


class CartLineItemModel(Base):
    __tablename__ = "cart_line_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id = Column(UUID(as_uuid=True), nullable=False)
    product_variant_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)
    image_name = Column(String(255))
    name = Column(String(100), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
