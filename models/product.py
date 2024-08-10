from pydantic import BaseModel
from models import user

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

class SpecBase(BaseModel):
    item: str
    description: str

class ProductOutBase(BaseModel):
    name: str
    price: int
    rating_avg: int
    review_count: int
    introduction: str
    specification: list[SpecBase]
    images: str
    file_size: int