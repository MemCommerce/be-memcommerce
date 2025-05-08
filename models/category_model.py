from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, func

from db import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
