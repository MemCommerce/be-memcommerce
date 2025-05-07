from uuid import uuid4

from sqlalchemy import Column, UUID, String

from db import Base


class ColorModel(Base):
    __tablename__ = "colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    label = Column(String(10), nullable=False)
    

