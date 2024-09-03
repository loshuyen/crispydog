from pydantic import BaseModel

class CartIn(BaseModel):
    id: int

class CartBase(BaseModel):
    id: int
    name: str
    price: int
    thumbnail: str

class CartOut(BaseModel):
    data: list[CartBase]