from fastapi import FastAPI
from app.core.config import get_settings
from sqlalchemy import text
from app.database.connection import engine

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

@app.get("/")
async def root():
    return {
        "message": "Block API is running",
        "environment": settings.environment,
    }

@app.get("/database-test")
async def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": result.scalar()
    }