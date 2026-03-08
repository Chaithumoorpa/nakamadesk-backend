from fastapi import FastAPI
from app.api import health
from app.db.session import engine

from app.db.base import Base
from app.models.user import User
from app.models.item import Item
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem

from app.api import auth
from app.api import items
from app.api import sales
from app.api import reports
from app.api import customers
from app.api import suppliers
from app.api import purchases



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NakamaDesk API",
    version="0.1.0"
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(sales.router)
app.include_router(reports.router)
app.include_router(customers.router)
app.include_router(suppliers.router)
app.include_router(purchases.router)

@app.get("/")
def root():
    return {"message": "NakamaDesk Backend Running"}

