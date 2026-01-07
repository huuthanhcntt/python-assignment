from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Movie
from app.dto import MovieDTO


class MovieRepository:
    """Repository for movie data access using database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _orm_to_movie(self, orm: Movie) -> MovieDTO:
        """Convert Movie ORM to MovieDTO dataclass."""
        data = orm.data or {}
        return MovieDTO(
            movie_name=data.get("movie_name", ""),
            movie_link=data.get("movie_link", ""),
            fshare_link=data.get("fshare_link", ""),
            original_title=data.get("original_title", ""),
            genre=data.get("genre", ""),
            year=data.get("year"),
            runtime=data.get("runtime"),
            rating=data.get("rating", 0.0),
            overview=data.get("overview", ""),
            poster_url=data.get("poster_url", ""),
            backdrop_url=data.get("backdrop_url", ""),
            tmdb_id=orm.tmdb_id or "",
            category_id=orm.category_id,
        )

    def _movie_to_orm(self, movie: MovieDTO, tenant: str) -> Movie:
        """Convert MovieDTO dataclass to Movie ORM."""
        return Movie(
            tenant=tenant,
            tmdb_id=movie.tmdb_id,
            category_id=movie.category_id,
            data={
                "movie_name": movie.movie_name,
                "movie_link": movie.movie_link,
                "fshare_link": movie.fshare_link,
                "original_title": movie.original_title,
                "genre": movie.genre,
                "year": movie.year,
                "runtime": movie.runtime,
                "rating": movie.rating,
                "overview": movie.overview,
                "poster_url": movie.poster_url,
                "backdrop_url": movie.backdrop_url,
            },
        )

    async def get_movies(
        self,
        tenant: str,
        limit: Optional[int] = None,
        genre: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[MovieDTO]:
        """Get movies for a tenant with optional filters."""
        query = select(Movie).where(Movie.tenant == tenant)

        # Apply JSONB filters
        if genre:
            query = query.where(
                Movie.data["genre"].astext.ilike(f"%{genre}%")
            )
        if year:
            query = query.where(
                Movie.data["year"].astext == str(year)
            )

        if limit:
            query = query.limit(limit)

        result = await self.session.execute(query)
        orm_movies = result.scalars().all()
        return [self._orm_to_movie(orm) for orm in orm_movies]

    async def get_movie_by_tmdb_id(
        self, tenant: str, tmdb_id: str
    ) -> Optional[MovieDTO]:
        """Get a single movie by TMDB ID within a tenant."""
        query = select(Movie).where(
            Movie.tenant == tenant, Movie.tmdb_id == tmdb_id
        )
        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()
        return self._orm_to_movie(orm) if orm else None

    async def create_movie(self, tenant: str, movie: MovieDTO) -> MovieDTO:
        """Create a new movie."""
        orm = self._movie_to_orm(movie, tenant)
        self.session.add(orm)
        await self.session.flush()
        await self.session.refresh(orm)
        return self._orm_to_movie(orm)

    async def create_movies_bulk(self, tenant: str, movies: List[MovieDTO]) -> int:
        """Bulk create movies for a tenant."""
        orm_movies = [self._movie_to_orm(movie, tenant) for movie in movies]
        self.session.add_all(orm_movies)
        await self.session.flush()
        return len(orm_movies)

    async def delete_all_movies(self, tenant: str) -> int:
        """Delete all movies for a tenant."""
        result = await self.session.execute(
            select(Movie).where(Movie.tenant == tenant)
        )
        movies = result.scalars().all()
        for movie in movies:
            await self.session.delete(movie)
        await self.session.flush()
        return len(movies)

    async def tenant_exists(self, tenant: str) -> bool:
        """Check if a tenant has any movies."""
        query = select(Movie).where(Movie.tenant == tenant).limit(1)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_all_tenants(self) -> List[str]:
        """Get list of all unique tenant names."""
        query = select(Movie.tenant).distinct()
        result = await self.session.execute(query)
        return list(result.scalars().all())
