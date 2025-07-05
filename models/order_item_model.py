from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, Integer, Numeric, String, TIMESTAMP, func

from db import Base


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    product_variant_id = Column(UUID(as_uuid=True), nullable=False)

    name = Column(String(100), nullable=False)             
    image_name = Column(String(255))                       
    price = Column(Numeric(10, 2), nullable=False)      
    quantity = Column(Integer, nullable=False, default=1)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
