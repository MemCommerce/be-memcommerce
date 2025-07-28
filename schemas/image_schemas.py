from pydantic import BaseModel


class BaseImage(BaseModel):
    pass


class TempImageCreate(BaseModel):
    base64_data: str


class TempImage(BaseModel):
    name: str
    url: str
