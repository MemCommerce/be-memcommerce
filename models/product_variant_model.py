from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db import Base


class ProductVariantModel(Base):
    __tablename__ = "product_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    product = relationship("ProductModel", backref="variants")

    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.id", ondelete="RESTRICT"), nullable=False)
    size_id = Column(UUID(as_uuid=True), ForeignKey("sizes.id", ondelete="RESTRICT"), nullable=False)

    color = relationship("ColorModel", backref="variants")
    size = relationship("SizeModel", backref="variants")

    price = Column(Numeric(10, 2), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
