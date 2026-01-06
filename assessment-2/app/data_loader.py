import csv
from pathlib import Path
from typing import List

from app.models import Movie


def parse_movie_row(row: dict[str, str]) -> Movie:
    # tolerant parsing for optional numeric fields
    def safe_int(val: str):
        try:
            return int(val)
        except Exception:
            return None

    def safe_float(val: str):
        try:
            return float(val)
        except Exception:
            return 0.0

    return Movie(
        movie_name=row.get("Movie Name", "").strip(),
        movie_link=row.get("Movie Link", "").strip(),
        fshare_link=row.get("Fshare Link", "").strip(),
        original_title=row.get("Original Title", "").strip(),
        genre=row.get("Genre", "").strip(),
        year=safe_int(row.get("Year", "")),
        runtime=row.get("Runtime", "").strip() or None,
        rating=safe_float(row.get("Rating", "")),
        overview=row.get("Overview", "").strip(),
        poster_url=row.get("Poster URL", "").strip(),
        backdrop_url=row.get("Backdrop URL", "").strip(),
        tmdb_id=row.get("TMDB ID", "").strip(),
    )


def load_movies_from_csv(path: Path) -> List[Movie]:
    movies: List[Movie] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append(parse_movie_row(row))
    return movies
