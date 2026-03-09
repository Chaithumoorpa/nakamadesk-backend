from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    total_amount = Column(Float, default=0.0)

    invoice_number = Column(String, unique=True, index=True)
    invoice_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    items = relationship("SaleItem", back_populates="sale")
    customer = relationship("Customer")
