from pydantic import BaseModel, EmailStr

class Deal(BaseModel):
    amount: int
    delivery_email: EmailStr | None
    products: list[int]
