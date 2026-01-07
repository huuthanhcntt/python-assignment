"""create categories table

Revision ID: c44c3366a677
Revises: 913dcf5a2d10
Create Date: 2026-01-07 14:46:54.312506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c44c3366a677'
down_revision: Union[str, Sequence[str], None] = '913dcf5a2d10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create categories table
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False, unique=True),
        sa.Column("parent_id", sa.Integer, nullable=True),
    )

    # Add self-referential foreign key
    op.create_foreign_key(
        "fk_categories_parent_id",
        "categories",
        "categories",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE"
    )

    # Add category_id column to movies table
    op.add_column(
        "movies",
        sa.Column("category_id", sa.Integer, nullable=True)
    )

    # Add foreign key from movies to categories
    op.create_foreign_key(
        "fk_movies_category_id",
        "movies",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL"
    )

    # Create index on category_id
    op.create_index("ix_movies_category_id", "movies", ["category_id"])

    # Insert example master data for categories
    categories_table = sa.table(
        "categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("parent_id", sa.Integer),
    )

    # Level 0: Root categories
    op.bulk_insert(
        categories_table,
        [
            {"id": 1, "name": "Action", "parent_id": None},
            {"id": 2, "name": "Drama", "parent_id": None},
            {"id": 3, "name": "Comedy", "parent_id": None},
            {"id": 4, "name": "Horror", "parent_id": None},
            {"id": 5, "name": "Science Fiction", "parent_id": None},
        ]
    )

    # Level 1: Subcategories
    op.bulk_insert(
        categories_table,
        [
            {"id": 6, "name": "Thriller", "parent_id": 1},
            {"id": 7, "name": "Adventure", "parent_id": 1},
            {"id": 8, "name": "Martial Arts", "parent_id": 1},
            {"id": 9, "name": "Romantic Drama", "parent_id": 2},
            {"id": 10, "name": "Historical Drama", "parent_id": 2},
            {"id": 11, "name": "Romantic Comedy", "parent_id": 3},
            {"id": 12, "name": "Dark Comedy", "parent_id": 3},
            {"id": 13, "name": "Psychological Horror", "parent_id": 4},
            {"id": 14, "name": "Slasher", "parent_id": 4},
            {"id": 15, "name": "Space Opera", "parent_id": 5},
            {"id": 16, "name": "Cyberpunk", "parent_id": 5},
        ]
    )

    # Level 2: Sub-subcategories
    op.bulk_insert(
        categories_table,
        [
            {"id": 17, "name": "Spy Thriller", "parent_id": 6},
            {"id": 18, "name": "Crime Thriller", "parent_id": 6},
            {"id": 19, "name": "Jungle Adventure", "parent_id": 7},
            {"id": 20, "name": "Kung Fu", "parent_id": 8},
            {"id": 21, "name": "Period Romance", "parent_id": 9},
            {"id": 22, "name": "War Drama", "parent_id": 10},
            {"id": 23, "name": "Black Comedy", "parent_id": 12},
            {"id": 24, "name": "Ghost Story", "parent_id": 13},
            {"id": 25, "name": "Dystopian", "parent_id": 16},
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key and column from movies table
    op.drop_index("ix_movies_category_id", table_name="movies")
    op.drop_constraint("fk_movies_category_id", "movies", type_="foreignkey")
    op.drop_column("movies", "category_id")

    # Drop categories table (cascade will handle foreign key)
    op.drop_constraint("fk_categories_parent_id", "categories", type_="foreignkey")
    op.drop_table("categories")
