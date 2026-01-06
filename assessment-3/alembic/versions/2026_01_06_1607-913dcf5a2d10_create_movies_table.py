"""create movies table

Revision ID: 913dcf5a2d10
Revises: 
Create Date: 2026-01-06 16:07:46.663551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '913dcf5a2d10'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # create movies table with JSONB payload
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tenant", sa.String(length=64), nullable=False),
        sa.Column("tmdb_id", sa.String(length=128), nullable=True),
        sa.Column(
            "data",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb")
        ),
    )

    # create indexes: tenant, tmdb_id, and a GIN index on the JSONB payload
    op.create_index("ix_movies_tenant", "movies", ["tenant"])
    op.create_index("ix_movies_tmdb_id", "movies", ["tmdb_id"])
    op.create_index("ix_movies_data_gin", "movies", ["data"], postgresql_using="gin")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_movies_data_gin", table_name="movies")
    op.drop_index("ix_movies_tmdb_id", table_name="movies")
    op.drop_index("ix_movies_tenant", table_name="movies")
    op.drop_table("movies")
