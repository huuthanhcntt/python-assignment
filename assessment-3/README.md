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

## 📄 Assessment 3 — Simple Movie Manager

This folder contains a FastAPI app with a layered architecture (API → Service → Repository → Database) that stores movies in PostgreSQL and exposes endpoints to list, fetch, and reload movies.

### Architecture

**Layered structure:**
- `app/models.py` — dataclass `Movie`
- `app/data_loader.py` — CSV parser
- `app/main.py` — FastAPI app initialization and middleware
- `app/api/movies.py` — Route handlers (API layer)
- `app/services/movie_service.py` — Business logic (Service layer)
- `app/repositories/movie_repo.py` — Database access (Repository layer)
- `app/db/` — Database models and session management
  - `base.py` — SQLAlchemy Base declarative
  - `session.py` — Async engine, session maker, and transaction management
  - `models/movie.py` — MovieORM model with JSONB data column

**API Endpoints:**
- `GET /movies` — list movies (requires tenant via `X-Tenant` header or `tenant` query param; optional `limit`, `genre`, `year` query params)
- `GET /movies/{tmdb_id}` — fetch a single movie by TMDB ID (tenant-aware)
- `POST /reload` — reload CSV for a tenant; supports multipart upload (`file`) or default tenant CSV file. Tenant must be specified.
- `GET /tenants` — list available tenants

**Multi-tenant support:**
- Movies are stored in PostgreSQL with a `tenant` column for isolation
- Filtering and queries are tenant-aware via the repository layer

Tenant selection
 - Tenant must be provided for tenant-aware endpoints either using the `X-Tenant` HTTP header or the `tenant` query parameter.

Run locally (two options)

1) Run with `uv` (if you use `uv` launcher):

```bash
uv run uvicorn app.main:app --reload --port 8000
```

2) Run in Docker:

```bash
docker compose up api
```

Run alembic migration

```bash
# Upgrade
docker compose up migrate

# Downgrade
docker compose run --rm migrate uv run alembic downgrade -1
# Or
docker compose run --rm migrate uv run alembic downgrade base
```