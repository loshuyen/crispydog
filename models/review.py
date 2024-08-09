from pydantic import BaseModel

class ReviewIn(BaseModel):
    rating: int
    content: str | None
    product_id: int