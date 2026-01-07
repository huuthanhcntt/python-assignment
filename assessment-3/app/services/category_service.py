from typing import List, Dict, Any, Optional

from app.repositories import CategoryRepository


class CategoryService:
    """Service layer for category business logic."""

    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def _build_nested_structure(self, flat_list: List[Dict[str, Any]], parent_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Convert flat list of categories to nested structure.

        Args:
            flat_list: Flat list of categories with parent_id
            parent_id: Parent ID to filter by (None for root)

        Returns:
            Nested list of categories
        """
        result = []
        for category in flat_list:
            if category["parent_id"] == parent_id:
                # Create category dict without parent_id and level
                cat_dict = {
                    "id": category["id"],
                    "name": category["name"]
                }

                # Recursively get subcategories
                subcategories = self._build_nested_structure(flat_list, category["id"])
                if subcategories:
                    cat_dict["subcategories"] = subcategories

                result.append(cat_dict)

        return result

    async def get_categories_hierarchy(self, max_level: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get hierarchical categories from level 0 and all subcategories.

        Args:
            max_level: Optional maximum hierarchy depth (None = unlimited, default: None)

        Returns:
            Nested list of categories with subcategories array
        """
        # Get flat list from repository
        flat_list = await self.repo.get_categories_hierarchy(max_level=max_level)

        # Convert to nested structure starting from root (parent_id = None)
        return self._build_nested_structure(flat_list, parent_id=None)
