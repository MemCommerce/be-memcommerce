from uuid import uuid4
from sqlalchemy import Column, UUID, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class ReturnItemModel(Base):
    __tablename__ = "return_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    return_id = Column(
        UUID(as_uuid=True), ForeignKey("returns.id", ondelete="CASCADE"), nullable=False
    )
    order_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("order_items.id", ondelete="CASCADE"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=True)

    return_request = relationship("ReturnModel", back_populates="items")
