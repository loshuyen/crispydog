from pydantic import BaseModel

class ReviewIn(BaseModel):
    rating: int
    content: str | None
    product_id: int

class Reviewer(BaseModel):
    id: int
    username: str

class Product(BaseModel):
    id: int
    name: str

class ReviewBase(BaseModel):
    id: int
    rating: int
    content: str
    updated_at: str
    reviewer: Reviewer

class ReviewListOut(BaseModel):
    next_page: int | None
    data: list[ReviewBase]

class ReviewOwnerBase(BaseModel):
    id: int
    rating: int
    content: str
    updated_at: str
    product: Product

class ReviewOwner(BaseModel):
    data: list[ReviewOwnerBase]