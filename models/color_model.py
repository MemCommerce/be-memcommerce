from uuid import uuid4

from sqlalchemy import Column, UUID, String, TIMESTAMP, func

from db import Base


class ColorModel(Base):
    __tablename__ = "colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(20), nullable=False)
    hex = Column(String(7), nullable=False)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
