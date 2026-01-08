from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Header, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories import MovieRepository, CategoryRepository
from app.services import MovieService, CategoryService

router = APIRouter()


def get_movie_service(session: AsyncSession = Depends(get_db)) -> MovieService:
    """Dependency to get MovieService instance."""
    repo = MovieRepository(session)
    return MovieService(repo)


def get_category_service(session: AsyncSession = Depends(get_db)) -> CategoryService:
    """Dependency to get CategoryService instance."""
    repo = CategoryRepository(session)
    return CategoryService(repo)


def get_tenant_from_request(
    tenant: Optional[str] = Query(None),
    x_tenant: Optional[str] = Header(None),
) -> str:
    """Extract tenant from request (header takes priority over query param)."""
    if not x_tenant and not tenant:
        raise HTTPException(
            status_code=400,
            detail="Tenant must be provided via X-Tenant header or tenant query parameter",
        )
    return x_tenant or tenant


@router.get("/movies", response_model=List[dict])
async def get_movies(
    limit: Optional[int] = Query(None, ge=1),
    genre: Optional[str] = None,
    year: Optional[int] = None,
    search: Optional[str] = Query(None, description="Search by movie name, original title, or overview"),
    tenant: str = Depends(get_tenant_from_request),
    service: MovieService = Depends(get_movie_service),
):
    """Get movies with optional filters and search."""
    # Check if tenant exists
    if not await service.tenant_exists(tenant):
        raise HTTPException(status_code=404, detail=f"Tenant not found: {tenant}")

    movies = await service.get_movies(tenant, limit, genre, year, search)
    return movies


@router.get("/movies/{tmdb_id}")
async def get_movie(
    tmdb_id: str,
    tenant: str = Depends(get_tenant_from_request),
    service: MovieService = Depends(get_movie_service),
):
    """Get a single movie by TMDB ID."""
    movie = await service.get_movie_by_tmdb_id(tenant, tmdb_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.post("/reload")
async def reload_csv(
    tenant: str = Query(
        ...,
        description="Target tenant. If no file is provided, available tenants are: `movies`, `tv_serials`, `trending`",
        example="trending",
    ),
    file: Optional[UploadFile] = File(
        None,
        description="Optional CSV file. If omitted, the system reloads data for the specified tenant."
    ),
    service: MovieService = Depends(get_movie_service),
):
    """Reload movies from CSV file for a specific tenant."""
    # Check if tenant exists (for file upload case)
    if file is not None:
        # Parse uploaded file
        content = await file.read()
        try:
            text = content.decode("utf-8")
        except Exception:
            raise HTTPException(
                status_code=400, detail="Uploaded file must be UTF-8 encoded CSV"
            )

        try:
            count = await service.reload_from_csv_content(tenant, text)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"Invalid CSV: {ve}")

        return {"loaded": count, "tenant": tenant}

    # No upload — load from default tenant csv file
    csv_path = Path(__file__).parent.parent / "csv" / f"{tenant}.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found: {csv_path}")

    try:
        count = await service.reload_from_csv_file(tenant, csv_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load CSV: {e}")

    return {"loaded": count, "tenant": tenant}


@router.get("/tenants", response_model=List[str])
async def list_tenants(service: MovieService = Depends(get_movie_service)):
    """Get list of all tenants."""
    return await service.get_all_tenants()


@router.get("/categories", response_model=List[dict])
async def get_categories(
    max_level: Optional[int] = Query(None, ge=0, description="Maximum hierarchy depth (None = unlimited)"),
    service: CategoryService = Depends(get_category_service),
):
    """
    Get hierarchical categories using recursive CTE with optional level limit.

    This endpoint demonstrates SQLAlchemy's recursive CTE capabilities.
    It returns categories in a nested array structure from level 0 (root)
    and all subcategories.

    Args:
        max_level: Optional maximum hierarchy depth (None = unlimited, default: None)

    Returns:
        Nested array of categories with:
        - id: Category ID
        - name: Category name
        - subcategories: Optional array of nested subcategories

    Example response:
    [
        {
            "id": 1,
            "name": "Action",
            "subcategories": [
                {
                    "id": 2,
                    "name": "Thriller",
                    "subcategories": [...]
                }
            ]
        }
    ]
    """
    return await service.get_categories_hierarchy(max_level=max_level)
