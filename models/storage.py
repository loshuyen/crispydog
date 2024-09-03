from pydantic import BaseModel

class Owner(BaseModel):
    id: int
    username: str

class Deal(BaseModel):
    id: int
    success: int

class Product(BaseModel):
    id: int
    name: str
    price: int
    thumbnail: str
    product_type: int
    owner: Owner

class Storage(BaseModel):
    download_endpoint: str
    file_type: str
    file_size: str
    created_at: str
    product: Product

class StorageOut(BaseModel):
    data: list[Storage]

class Commission(BaseModel):
    id: int
    photo_url: str
    is_accepted: int
    is_paid: int
    is_delivered: int
    is_downloaded: int
    updated_at: str
    deal: Deal
    product: Product

class CommissionOut(BaseModel):
    data: list[Commission]

class CommissionUrl(BaseModel):
    file_url: str

class CommissionOutSingle(BaseModel):
    data: Commission