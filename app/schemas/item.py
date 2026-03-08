from pydantic import BaseModel, field_validator
from typing import Optional

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
        if v is not None and not (0 <= v <= 28):
            raise ValueError("gst_percent must be between 0 and 28")
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
