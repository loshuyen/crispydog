from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    owner_name: str
    rating_avg: float = 0.0
    review_count: int = 0
    price: int
    thumbnail_url: str | None = None

class Product(BaseModel):
    data: list[ProductBase]