from typing import Optional

from pydantic import BaseModel, field_validator

from app.core.constants import GST_ALLOWED


class ItemCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    hsn_code: Optional[str] = None
    gst_percent: Optional[float] = 0.0

    @field_validator("gst_percent")
    @classmethod
    def validate_gst(cls, v):
        if v is not None and v not in GST_ALLOWED:
            raise ValueError(f"gst_percent must be one of {GST_ALLOWED}")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("price must not be negative")
        return v

    @field_validator("stock_quantity")
    @classmethod
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError("stock_quantity must not be negative")
        return v


class ItemResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    hsn_code: Optional[str] = None
    gst_percent: Optional[float] = 0.0

    class Config:
        from_attributes = True
