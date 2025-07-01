# pyright: reportCallIssue=false

from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_serializer


class UserBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="First name of the user",
        example="John",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Last name of the user",
        example="Doe",
    )
    email: EmailStr = Field(
        ..., description="Email of the user", example="john_doe@example.com"
    )


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
