from fastapi import FastAPI, HTTPException, Query, Request, Header, Depends, UploadFile, File
from pathlib import Path
from typing import List, Optional, Dict
import csv
import io
import time
import logging
import os

from app.models import Movie
from app.data_loader import load_movies_from_csv, parse_movie_row

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("assessment-2")

app = FastAPI(title="Simple Movie Manager")


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    elapsed = time.monotonic() - start
    # add timing header (seconds)
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    # log method, path, status and elapsed
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} in {elapsed:.6f}s")
    return response

# multi-tenant in-memory store: tenant -> list[Movie]
MOVIES_STORE: Dict[str, List[Movie]] = {}
DEFAULT_TENANT = "movies"


@app.on_event("startup")
def startup_load():
    global MOVIES_STORE
    # default CSV path relative to this folder
    base = Path(__file__).parent / "csv"
    # load known tenants if present
    MOVIES_STORE.clear()
    # default tenant
    default_path = base / "movies.csv"
    if default_path.exists():
        MOVIES_STORE["movies"] = load_movies_from_csv(default_path)
    # optional tv_serials tenant
    tv_serials_path = base / "tv_serials.csv"
    if tv_serials_path.exists():
        MOVIES_STORE["tv_serials"] = load_movies_from_csv(tv_serials_path)


def get_tenant_store(tenant: Optional[str] = None, x_tenant: Optional[str] = Header(None)) -> List[Movie]:
    """Dependency that returns the movie list for the requested tenant.

    Priority: `x-tenant` header -> `tenant` query param -> default tenant
    """
    # require explicit tenant selection
    if not x_tenant and not tenant:
        raise HTTPException(
            status_code=400,
            detail="Tenant must be provided via X-Tenant header or tenant query parameter",
        )

    sel = x_tenant or tenant
    store = MOVIES_STORE.get(sel)
    if store is None:
        raise HTTPException(status_code=404, detail=f"Tenant not found: {sel}")
    return store


@app.get("/movies", response_model=List[dict])
def get_movies(
    limit: Optional[int] = Query(None, ge=1),
    genre: Optional[str] = None,
    year: Optional[int] = None,
    tenant_store: List[Movie] = Depends(get_tenant_store),
):
    results = tenant_store
    if genre:
        results = [m for m in results if genre.lower() in (m.genre or "").lower()]
    if year:
        results = [m for m in results if m.year == year]
    if limit:
        results = results[:limit]
    # convert dataclass to dict for JSON
    return [m.__dict__ for m in results]


@app.get("/movies/{tmdb_id}")
def get_movie(tmdb_id: str, tenant_store: List[Movie] = Depends(get_tenant_store)):
    for m in tenant_store:
        if m.tmdb_id == tmdb_id:
            return m.__dict__
    raise HTTPException(status_code=404, detail="Movie not found")


@app.post("/reload")
async def reload_csv(
    tenant: str,
    file: Optional[UploadFile] = File(None),
):
    # allow reloading into a specific tenant, but only whitelist accepted tenants
    if tenant not in MOVIES_STORE:
        raise HTTPException(status_code=400, detail=f"Unsupported tenant: {tenant}")

    # If an uploaded file is provided, parse it in-memory and validate CSV
    if file is not None:
        content = await file.read()
        try:
            text = content.decode("utf-8")
        except Exception:
            raise HTTPException(status_code=400, detail="Uploaded file must be UTF-8 encoded CSV")

        try:
            stream = io.StringIO(text)
            reader = csv.DictReader(stream)
            # basic validation: ensure headers present
            required = {"Movie Name", "TMDB ID"}
            if not reader.fieldnames:
                raise ValueError("No CSV header found")
            headers = set(reader.fieldnames)
            if not required.issubset(headers):
                raise ValueError(f"Missing required columns: {required - headers}")

            movies = []
            for row in reader:
                try:
                    movies.append(parse_movie_row(row))
                except Exception as e:
                    raise ValueError(f"Failed to parse row: {e}")

        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"Invalid CSV: {ve}")

        MOVIES_STORE[tenant] = movies
        return {"loaded": len(MOVIES_STORE[tenant]), "tenant": tenant}

    # no upload — load from default tenant csv file
    csv_path = Path(__file__).parent / "csv" / f"{tenant}.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found: {csv_path}")
    MOVIES_STORE[tenant] = load_movies_from_csv(csv_path)
    return {"loaded": len(MOVIES_STORE[tenant]), "tenant": tenant}


@app.get("/tenants", response_model=List[str])
def list_tenants():
    return list(MOVIES_STORE.keys())


@app.post("/tenants")
def add_tenant(tenant: str):
    if tenant in MOVIES_STORE:
        raise HTTPException(status_code=400, detail=f"Tenant already exists: {tenant}")
    MOVIES_STORE[tenant] = []
    return {"message": f"Tenant added: {tenant}"}