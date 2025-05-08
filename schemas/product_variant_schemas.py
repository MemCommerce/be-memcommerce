from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ProductVariantBase(BaseModel):
    price: float


class ProductVariantData(ProductVariantBase):
    product_id: str
    color_id: str
    size_id: str


class ProductVariant(ProductVariantBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    color_id: UUID
    size_id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("product_id")
    def serialize_product_id(self, product_id: UUID, _info):
        return str(product_id)
    
    @field_serializer("color_id")
    def serialize_color_id(self, color_id: UUID, _info):
        return str(color_id)
    
    @field_serializer("size_id")
    def serialize_size_id(self, size_id: UUID, _info):
        return str(size_id)
