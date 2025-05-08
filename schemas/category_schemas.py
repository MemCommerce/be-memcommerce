from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryData(CategoryBase):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
