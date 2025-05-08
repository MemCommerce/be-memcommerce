from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

class SizeBase(BaseModel):
    label: str


class SizeData(SizeBase):
    pass


class Size(SizeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
