# Project: FastAPI Application

## Stack
- Python 3.11+ (running on 3.14 locally)
- FastAPI for the web framework
- PostgreSQL for the database
- SQLAlchemy 2.0 (sync) for the ORM — `create_engine` + `sessionmaker`, not async yet
- Alembic for database migrations
- Pydantic v2 + pydantic-settings for config (`app/core/config.py`)
- Uvicorn as the ASGI server

Not yet added: JWT auth libs (python-jose), Passlib, Pytest/httpx. `jwt_secret_key`/`jwt_algorithm` exist in config but nothing consumes them yet.

## Commands
- `uvicorn app.main:app --reload` — start dev server (port 8000)
- `alembic upgrade head` — apply latest migrations
- `alembic revision --autogenerate -m "description"` — generate new migration

No test suite exists yet, so there is no test command.

## Project Structure (current)
- `app/core/config.py` — Pydantic `Settings`, loaded from `.env` via `get_settings()`
- `app/database/base.py` — `Base(DeclarativeBase)`
- `app/database/connection.py` — module-level SQLAlchemy `engine`
- `app/database/session.py` — `SessionLocal` + `get_db()` FastAPI dependency
- `app/models/` — SQLAlchemy models (`user.py` so far)
- `app/main.py` — FastAPI app instance and routes (routes currently live directly in `main.py`)
- `alembic/` — migration env and versions

Not yet created: `routers/`, `schemas/`, `services/`, `tests/`. When these are introduced, keep routers/models/schemas/services in separate files per the Behavior Rules below.

## Coding Conventions
- Route handlers and DB calls are currently sync (`Session`, `create_engine`) — do not switch to async without discussing it first, since that's an architectural change
- Use Pydantic schemas for request/response shaping once `schemas/` exists; don't inline validation in routes
- Passwords must always be hashed — never store plaintext (no hashing utility exists yet, needs Passlib)
- JWT tokens must always be validated before accessing protected routes (no auth implemented yet)
- Keep routers, models, schemas, and services in separate files as they're introduced

## Behavior Rules
- Never modify .env or .env.local files
- Never install packages without confirming with me first
- Always run pytest after making any changes
- Never hardcode secrets, credentials, or tokens in any file
- Stay within this project directory at all times
- Ask before making structural or architectural changes
- When adding a new feature always create: router + schema + service + test
