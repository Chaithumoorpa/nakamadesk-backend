from fastapi import FastAPI
from app.api import health
from app.db.session import engine

from app.db.base import Base
from app.models.user import User
from app.models.item import Item

from app.api import auth
from app.api import items



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NakamaDesk API",
    version="0.1.0"
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(items.router)

@app.get("/")
def root():
    return {"message": "NakamaDesk Backend Running"}

