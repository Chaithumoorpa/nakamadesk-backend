from pydantic import BaseModel
from typing import List
from datetime import datetime

class SaleItemCreate(BaseModel):
    item_id: int
    quantity: int

class SaleCreate(BaseModel):
    items: List[SaleItemCreate]

class SaleItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    price_at_sale: float

    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    id: int
    total_amount: float
    created_at: datetime
    items: List[SaleItemResponse] = []

    class Config:
        from_attributes = True
