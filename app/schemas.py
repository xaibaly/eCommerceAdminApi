from pydantic import BaseModel
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float

class InventoryUpdate(BaseModel):
    product_id: int
    stock_level: int

class SalesData(BaseModel):
    product_id: int
    quantity: int
    date: datetime
