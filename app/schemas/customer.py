from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
