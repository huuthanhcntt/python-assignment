from dataclasses import dataclass
from typing import Optional


@dataclass
class MovieDTO:
    """Data Transfer Object for Movie."""
    movie_name: str
    movie_link: str
    fshare_link: str
    original_title: str
    genre: str
    year: Optional[int]
    runtime: Optional[str]
    rating: float
    overview: str
    poster_url: str
    backdrop_url: str
    tmdb_id: str
    category_id: Optional[int] = None
