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
