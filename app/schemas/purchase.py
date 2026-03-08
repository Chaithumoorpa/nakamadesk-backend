from pydantic import BaseModel
from typing import List
from datetime import datetime

class PurchaseItemCreate(BaseModel):
    item_id: int
    quantity: int
    cost_price: float

class PurchaseCreate(BaseModel):
    supplier_id: int
    items: List[PurchaseItemCreate]

class PurchaseItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    cost_price: float

    class Config:
        from_attributes = True

class PurchaseResponse(BaseModel):
    id: int
    supplier_id: int
    total_amount: float
    created_at: datetime
    items: List[PurchaseItemResponse] = []

    class Config:
        from_attributes = True
