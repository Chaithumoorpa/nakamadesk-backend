from fastapi import FastAPI
from app.api import health

app = FastAPI(
    title="NakamaDesk API",
    version="0.1.0"
)

app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "NakamaDesk Backend Running"}