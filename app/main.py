from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.core.exceptions import ConflictError, NotFoundError, PermissionDeniedError
from sqlalchemy import text
from app.database.connection import engine
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.training_blocks import router as training_blocks_router
from app.api.training_weeks import router as training_weeks_router
from app.api.workout_types import router as workout_types_router
from app.api.workouts import router as workouts_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(training_blocks_router)
app.include_router(training_weeks_router)
app.include_router(workout_types_router)
app.include_router(workouts_router)


@app.exception_handler(NotFoundError)
def handle_not_found(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(PermissionDeniedError)
def handle_permission_denied(request: Request, exc: PermissionDeniedError):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
def handle_conflict(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

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