from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str   # Name of the product required
    price: str  # Price of the product required
    image: str  # Image url of the product required
    weight: str # Weight of the product

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductPathc(ProductBase):
    name: Optional[str]
    price: Optional[str]
    image: Optional[str]
    weight: Optional[str]

class Product(ProductBase):
    id: str

    class Config:
        orm_mode = True