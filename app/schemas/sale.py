from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


class SaleItemCreate(BaseModel):
    item_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v):
        if v is not None and v <= 0:
            raise ValueError("quantity must be greater than zero")
        return v


class SaleCreate(BaseModel):
    items: List[SaleItemCreate]
    customer_id: Optional[int] = None


class SaleItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    price_at_sale: float
    gst_percent: float = 0.0
    cgst_amount: float = 0.0
    sgst_amount: float = 0.0
    total_price: float = 0.0

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    total_amount: float
    created_at: datetime
    customer_id: Optional[int] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[datetime] = None
    items: List[SaleItemResponse] = []

    class Config:
        from_attributes = True
