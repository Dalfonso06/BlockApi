from fastapi import FastAPI
from app.core.config import get_settings
from sqlalchemy import text
from app.database.connection import engine
from app.api.auth import router as auth_router
from app.api.users import router as users_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(auth_router)
app.include_router(users_router)

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