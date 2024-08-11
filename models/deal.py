from pydantic import BaseModel, EmailStr

class DealBase(BaseModel):
    products: list[int]
    amount: int
    delivery_email: EmailStr | None

class Contact(BaseModel):
    name: str
    phone_number: str
    email: EmailStr

class Deal(BaseModel):
    prime: str
    deal: DealBase
    contact: Contact
