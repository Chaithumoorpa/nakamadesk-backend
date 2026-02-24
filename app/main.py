from fastapi import FastAPI
from app.api import health
from app.db.session import engine

app = FastAPI(
    title="NakamaDesk API",
    version="0.1.0"
)

app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "NakamaDesk Backend Running"}

@app.get("/db-check")
def db_check():
    try:
        connection = engine.connect()
        connection.close()
        return {"database": "connected"}
    except Exception as e:
        return {"error": str(e)}