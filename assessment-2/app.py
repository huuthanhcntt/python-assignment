from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
from typing import List, Optional

from models import Movie
from data_loader import load_movies_from_csv

app = FastAPI(title="Simple Movie Manager")

# in-memory store
MOVIES: List[Movie] = []


@app.on_event("startup")
def startup_load():
    global MOVIES
    # default CSV path relative to this folder
    default = Path(__file__).parent / "csv" / "movies.csv"
    csv_path = default if default.exists() else Path("csv/movies.csv")
    if csv_path.exists():
        MOVIES = load_movies_from_csv(csv_path)
    else:
        MOVIES = []


@app.get("/movies", response_model=List[dict])
def get_movies(
    limit: Optional[int] = Query(None, ge=1),
    genre: Optional[str] = None,
    year: Optional[int] = None,
):
    results = MOVIES
    if genre:
        results = [m for m in results if genre.lower() in (m.genre or "").lower()]
    if year:
        results = [m for m in results if m.year == year]
    if limit:
        results = results[:limit]
    # convert dataclass to dict for JSON
    return [m.__dict__ for m in results]


@app.get("/movies/{tmdb_id}")
def get_movie(tmdb_id: str):
    for m in MOVIES:
        if m.tmdb_id == tmdb_id:
            return m.__dict__
    raise HTTPException(status_code=404, detail="Movie not found")


@app.post("/reload")
def reload_csv(path: Optional[str] = None):
    global MOVIES
    csv_path = Path(path) if path else (Path(__file__).parent / "csv" / "movies.csv")
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found: {csv_path}")
    MOVIES = load_movies_from_csv(csv_path)
    return {"loaded": len(MOVIES)}
