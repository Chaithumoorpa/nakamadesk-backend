from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
