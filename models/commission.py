from pydantic import BaseModel, EmailStr

class Commission(BaseModel):
    id: int

class Contact(BaseModel):
    name: str
    phone_number: str
    email: EmailStr

class Pay(BaseModel):
    prime: str
    commission_id: int
    contact: Contact

class Deal(BaseModel):
    id: int
    success: int

class Product(BaseModel):
    id: int
    name: str
    price: int
    thumbnail: str

class Buyer(BaseModel):
    id: int
    username: str

class CommissionOutBase(BaseModel):
    id: int
    photo_url: str
    file_url: str | None
    is_accepted: int
    is_paid: int
    is_delivered: int
    is_downloaded: int
    updated_at: str
    deal: Deal
    product: Product
    buyer: Buyer

class CommissionOutList(BaseModel):
    data: list[CommissionOutBase]

class CommissionOut(BaseModel):
    data: CommissionOutBase

class CommissionLinePayUrl(BaseModel):
    payment_url: str