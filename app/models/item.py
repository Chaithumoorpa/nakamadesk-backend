from sqlalchemy import Column, Float, Integer, String

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    hsn_code = Column(String)
    gst_percent = Column(Float, default=0.0)
