from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, func, TEXT, Integer

from db import Base


class ReviewModel(Base):
   __tablename__ = "reviews"

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
   
   product_variant_id = Column(
       UUID(as_uuid=True),
       ForeignKey("product_variants.id", ondelete="CASCADE"),
       nullable=False,
   )

   order_item_id = Column(
       UUID(as_uuid=True),
       ForeignKey("order_items.id", ondelete="CASCADE"),
       nullable=False,
   )
   
   user_id = Column(
       UUID(as_uuid=True),
       ForeignKey("users.id", ondelete="CASCADE"),
       nullable=False,
   )
   
   rating = Column(Integer, nullable=False)
   title = Column(String(100), nullable=True)
   content = Column(TEXT, nullable=True)
   
   created_at = Column(TIMESTAMP, server_default=func.now())
   updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
