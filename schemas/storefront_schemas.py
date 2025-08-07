from pydantic import BaseModel

class StorefrontVariant(BaseModel):
    id: str
    size: str
    size_id: str
    color: str
    color_hex: str
    color_id: str
    price: float
    image_url: str


class SFReview(BaseModel):
    id: str
    rating: int
    title: str | None
    content: str | None
    product_variant_id: str
    reviewer_name: str


class StorefrontProduct(BaseModel):
    id: str
    name: str
    brand: str
    description: str
    category_name: str
    variants: list[StorefrontVariant]
    


class StorefrontData(BaseModel):
    products: list[StorefrontProduct]


class SFProductWithReviews(StorefrontProduct):
    reviews: list[SFReview]
