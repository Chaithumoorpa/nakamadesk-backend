from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

    class Config:
        from_attributes = True
