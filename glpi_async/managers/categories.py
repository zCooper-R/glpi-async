from .base import BaseManager


class CategoryManager(BaseManager):
    def __init__(self, api):
        super().__init__(api, 'ITILCategory')

    async def list(self):
        """Простой список всех категорий без сортировки."""
        return await self.api.get(f"{self.item_name}")

    async def list_sorted_by_name(self):
        """Отсортированный список категорий по имени (с серверной сортировкой)."""
        params = {
            "uid_cols": True,
            "order": "ASC",
            "range": "0-20"
        }
        result = await self.api.get(f"/search/{self.item_name}", params=params)
        return result

    async def get_name(self, category_id: int) -> str:
        """Получение названия категории по ID."""
        category = await self.api.get(f"{self.item_name}/{category_id}")
        return category.get("name")


