from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ProductBase(BaseModel):
    name: str
    brand: str
    description: str


class ProductData(ProductBase):
    category_id: str


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    category_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("category_id")
    def serialize_category_id(self, category_id: UUID, _info):
        return str(category_id)
