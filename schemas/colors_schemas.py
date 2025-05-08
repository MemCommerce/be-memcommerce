from pydantic import BaseModel


class ColorBase(BaseModel):
    name: str
    hex: str


class ColorData(ColorBase):
    pass
