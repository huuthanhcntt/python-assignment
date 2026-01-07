import csv
import io
from pathlib import Path
from typing import List, Optional

from app.repositories import MovieRepository
from app.data_loader import parse_movie_row, load_movies_from_csv


class MovieService:
    """Service layer for movie business logic."""

    def __init__(self, repo: MovieRepository):
        self.repo = repo

    async def get_movies(
        self,
        tenant: str,
        limit: Optional[int] = None,
        genre: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[dict]:
        """Get movies with optional filters, returning dicts for JSON serialization."""
        movies = await self.repo.get_movies(tenant, limit, genre, year)
        return [movie.__dict__ for movie in movies]

    async def get_movie_by_tmdb_id(self, tenant: str, tmdb_id: str) -> Optional[dict]:
        """Get a single movie by TMDB ID."""
        movie = await self.repo.get_movie_by_tmdb_id(tenant, tmdb_id)
        return movie.__dict__ if movie else None

    async def tenant_exists(self, tenant: str) -> bool:
        """Check if a tenant exists."""
        return await self.repo.tenant_exists(tenant)

    async def get_all_tenants(self) -> List[str]:
        """Get list of all tenant names."""
        return await self.repo.get_all_tenants()

    async def reload_from_csv_file(self, tenant: str, csv_path: Path) -> int:
        """Load movies from a CSV file path and replace tenant data."""
        movies = load_movies_from_csv(csv_path)

        # Delete existing movies for this tenant
        await self.repo.delete_all_movies(tenant)

        # Bulk insert new movies
        count = await self.repo.create_movies_bulk(tenant, movies)
        return count

    async def reload_from_csv_content(self, tenant: str, csv_content: str) -> int:
        """Load movies from CSV content string and replace tenant data."""
        # Validate CSV format
        stream = io.StringIO(csv_content)
        reader = csv.DictReader(stream)

        if not reader.fieldnames:
            raise ValueError("No CSV header found")

        required = {"Movie Name", "TMDB ID"}
        headers = set(reader.fieldnames)
        if not required.issubset(headers):
            raise ValueError(f"Missing required columns: {required - headers}")

        # Parse all rows
        movies = []
        for row in reader:
            try:
                movies.append(parse_movie_row(row))
            except Exception as e:
                raise ValueError(f"Failed to parse row: {e}")

        # Delete existing movies for this tenant
        await self.repo.delete_all_movies(tenant)

        # Bulk insert new movies
        count = await self.repo.create_movies_bulk(tenant, movies)
        return count
