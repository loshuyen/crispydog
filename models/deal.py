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

class Owner(BaseModel):
    id: int
    username: str

class productBase(BaseModel):
    id: int
    name: str
    price: int
    owner: Owner

class DealOutBase(BaseModel):
    id: int
    amount: int
    delivery_email: EmailStr | None
    success: int
    created_at: str
    products: list[productBase]

class DealOut(BaseModel):
    data: list[DealOutBase]

class Payment(BaseModel):
    method: str
    status: int
    message: str

class PayBase(BaseModel):
    number: str
    payment: Payment

class PayResultOut(BaseModel): 
    data: PayBase

class PaymentUrl(BaseModel):
    payment_url: str