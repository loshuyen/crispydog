from pydantic import BaseModel
from models import user

class Owner(BaseModel):
    id: int
    username: str

class ProductBase(BaseModel):
    id: int
    name: str
    rating_avg: float = 0.0
    review_count: int = 0
    price: int
    thumbnail_url: str | None = None
    product_type: int
    owner: Owner

class ProductDetailBase(ProductBase):
    introduction: str
    specification: str | None = None
    images: str
    file_size: float | None = None

class ProductId(BaseModel):
    id: int

class ProductOwnerBase(BaseModel):
    id: int
    name: str
    price: int
    thumbnail: str | None = None
    product_type: int
    introduction: str
    specification: str | None = None
    images: str
    status: int
    stock: int
    rating_avg: float = 0.0
    review_count: int = 0

class ProductOwnerPublicBase(BaseModel):
    id: int
    name: str
    price: int
    product_type: int
    rating_avg: float = 0.0
    review_count: int = 0
    introduction: str
    specification: str | None = None
    images: str
    file_size: float | None = None
    thumbnail: str | None = None

class Product(BaseModel):
    data: list[ProductBase]

class ProductDetail(BaseModel):
    data: ProductDetailBase

class ProductOwner(BaseModel):
    data: list[ProductOwnerBase]

class ProductOwnerPublic(BaseModel):
    data: list[ProductOwnerPublicBase]