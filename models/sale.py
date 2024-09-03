from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: int
    thumbnail: str

class Buyer(BaseModel):
    id: int
    username: str

class SaleBase(BaseModel):
    id: int
    created_at: str
    buyer: Buyer

class Sale(SaleBase):
    product: Product

class SaleList(BaseModel):
    data: list[Sale]

class ProductSale(Product):
    status: int
    sales_count: int
    sales: list[SaleBase]

class ProductSaleData(BaseModel):
    data: ProductSale