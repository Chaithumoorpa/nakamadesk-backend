from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, nullable=False)
    price_at_sale = Column(Float, nullable=False)
    gst_percent = Column(Float, default=0.0)
    cgst_amount = Column(Float, default=0.0)
    sgst_amount = Column(Float, default=0.0)
    total_price = Column(Float, default=0.0)

    sale = relationship("Sale", back_populates="items")
    item = relationship("Item")
