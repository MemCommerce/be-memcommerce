from pydantic import BaseModel


class StorefrontVariant(BaseModel):
    id: str
    size: str
    size_id: str
    color: str
    color_id: str
    price: float


class StorefrontProduct(BaseModel):
    id: str
    name: str
    brand: str
    description: str
    category_name: str
    variants: list[StorefrontVariant]


class StorefrontData(BaseModel):
    products: list[StorefrontProduct]
