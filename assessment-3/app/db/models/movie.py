from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class Movie(Base):
    """Movie ORM model."""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    tenant = Column(String(64), nullable=False)
    tmdb_id = Column(String(128))
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )
    # flexible JSON payload stored as JSONB (indexed via GIN in migrations for efficient querying)
    data = Column(JSONB, nullable=False)
