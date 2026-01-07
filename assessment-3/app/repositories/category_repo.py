from typing import List, Dict, Any, Optional

from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Movie, Category


class CategoryRepository:
    """Repository for category data access using database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _build_category_hierarchy_cte(self, max_level: Optional[int] = None):
        """
        Build a recursive CTE for category hierarchy with optional level limit.

        This CTE can be reused in any query that needs hierarchical category data.
        It includes:
        - id: Category ID
        - name: Category name
        - parent_id: Parent category ID
        - level: Hierarchy depth (0 for root)

        Args:
            max_level: Optional maximum hierarchy depth (None = unlimited, default: None)

        Returns:
            SQLAlchemy CTE object representing the category hierarchy
        """
        # Base case: root categories (no parent)
        base_cte = (
            select(
                Category.id,
                Category.name,
                Category.parent_id,
                literal(0).label("level")
            )
            .where(Category.parent_id.is_(None))
        ).cte(name="category_hierarchy", recursive=True)

        # Recursive case: child categories
        recursive_query = (
            select(
                Category.id,
                Category.name,
                Category.parent_id,
                (base_cte.c.level + 1).label("level")
            )
            .join(base_cte, Category.parent_id == base_cte.c.id)
        )

        # Apply max_level limit if specified
        if max_level is not None:
            recursive_query = recursive_query.where(base_cte.c.level < max_level)

        # Combine base and recursive parts
        category_cte = base_cte.union_all(recursive_query)
        return category_cte

    async def get_categories_hierarchy(self, max_level: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get hierarchical categories using recursive CTE with optional level limit.

        This query demonstrates SQLAlchemy's CTE capabilities for hierarchical data.
        It builds a category hierarchy from level 0 (root) and all subcategories.

        Args:
            max_level: Optional maximum hierarchy depth (None = unlimited, default: None)

        Returns:
            Flat list of dictionaries containing:
            - id: Category ID
            - name: Category name
            - parent_id: Parent category ID (None for root)
            - level: Hierarchy depth (0 for root)
        """
        # Get reusable category hierarchy CTE
        category_cte = self._build_category_hierarchy_cte(max_level=max_level)

        # Final query: select from CTE
        query = (
            select(
                category_cte.c.id,
                category_cte.c.name,
                category_cte.c.parent_id,
                category_cte.c.level
            )
            .order_by(category_cte.c.level, category_cte.c.id)
        )

        result = await self.session.execute(query)
        rows = result.all()

        return [
            {
                "id": row.id,
                "name": row.name,
                "parent_id": row.parent_id,
                "level": row.level,
            }
            for row in rows
        ]
