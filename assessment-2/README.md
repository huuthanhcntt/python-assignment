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

## 📄 Assessment 2 — Simple Movie Manager

This folder contains a tiny FastAPI app that loads a movie CSV into memory and exposes simple endpoints to list and fetch movies.

Files:
- `models.py` — dataclass `Movie`
- `data_loader.py` — CSV -> `Movie` loader
- `app.py` — FastAPI app with endpoints:
    - `GET /movies` — list movies (optional `limit`, `genre`, `year` query params)
    - `GET /movies/{tmdb_id}` — fetch a single movie by TMDB ID
    - `POST /reload` — reload CSV (optional `path` body param)

Run locally:

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app:app --reload --port 8000
```

Place your CSV at `assessment-2/csv/movies.csv` or call `/reload` with a path.
