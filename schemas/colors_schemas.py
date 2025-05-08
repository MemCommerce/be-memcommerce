from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ColorBase(BaseModel):
    name: str
    hex: str


class ColorData(ColorBase):
    pass


class Color(ColorBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
