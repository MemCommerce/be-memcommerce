from uuid import uuid4

from sqlalchemy import Column, UUID, String, TIMESTAMP, Numeric, func

from db import Base


class WishlistItemModel(Base):
    __tablename__ = "wishlist_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image_name = Column(String(255))
    name = Column(String(100), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
