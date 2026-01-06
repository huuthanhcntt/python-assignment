## 📅 Week 1.2: AsyncIO & FastAPI (The Engine)
- **Goal**: Master the "Event Loop" and move away from the PHP mentality.
- **AsyncIO Deep Dive**:
    - Coroutines (`async def`) vs. Tasks (`asyncio.create_task`).
    - Avoiding blocking calls (e.g., never use `time.sleep()` in FastAPI).
- **FastAPI Framework**:
    - DI System: Mapping Laravel's Service Container to [FastAPI's Depends](https://fastapi.tiangolo.com/tutorial/dependencies/%5D(https://fastapi.tiangolo.com/tutorial/dependencies/)).
    - Data Validation: Using [Pydantic v2](https://docs.pydantic.dev/latest/) for strict schema enforcement (replaces FormRequests).
 - **Assessment 2**:
    - Task: Create a FastAPI middleware that logs request execution time and a protected route that uses a custom DI provider for multi-tenant database switching. Create a simple student management system
    - Reference: [FastAPI "To async or not to async"](https://fastapi.tiangolo.com/async/)

## 📅 Week 2: SQLAlchemy 2.0 & Postgres (The Persistence)
- **Goal**: Shift from Active Record (Eloquent) to Data Mapper (SQLAlchemy).
- **Advanced SQLAlchemy**:
    - The Unit of Work: Mastering the `AsyncSession` and explicit transaction boundaries (commit/rollback).
    - N+1 Prevention: Using `selectinload` and `joinedload` (replaces `$user->with('posts')`).
- **Postgres in 2025**:
    - Working with JSONB for flexible schemas and GIN indexes.
    - Database migrations using [Alembic](https://alembic.sqlalchemy.org/en/latest/).
- **Assessment 3**:
    - Task: Write a complex query using SQLAlchemy's CTE (Common Table Expressions) to generate a hierarchical report (e.g., categories and subcategories) in a single async request.
    - Reference: [SQLAlchemy 2.0 Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

## 📄 Assessment 2 & 3 — Simple Movie Manager

This folder contains a tiny FastAPI app that loads a movie CSV into memory and exposes simple endpoints to list and fetch movies.

Files:
- `app/models.py` — dataclass `Movie`
- `app/data_loader.py` — CSV -> `Movie` loader
- `app/main.py` — FastAPI app with endpoints:
    - `GET /movies` — list movies (requires tenant via `X-Tenant` header or `tenant` query param; optional `limit`, `genre`, `year` query params)
    - `GET /movies/{tmdb_id}` — fetch a single movie by TMDB ID (tenant-aware)
    - `POST /reload` — reload CSV for a tenant; supports multipart upload (`file`) or default tenant CSV file. Tenant must be specified.
    - `GET /tenants` — list available tenants
    - `POST /tenants` — create an empty tenant

This app supports simple multi-tenant behavior via CSV files placed in `assessment-2/app/csv/`:

- `movies.csv` → tenant `movies`
- `tv_serials.csv` → tenant `tv_serials`

Tenant selection
 - Tenant must be provided for tenant-aware endpoints either using the `X-Tenant` HTTP header or the `tenant` query parameter.

Run locally (two options)

1) Run with `uv` (if you use `uv` launcher):

```bash
uv run uvicorn app.main:app --reload --port 8000
```

2) Run in Docker:

```bash
docker compose up
```