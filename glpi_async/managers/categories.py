from .base import BaseManager


class CategoryManager(BaseManager):
    def __init__(self, api):
        super().__init__(api, 'ITILCategory')

    async def list(self):
        return await self.api.get(f"{self.item_name}")

    async def get_name(self, category_id: int) -> str:
        """Получение названия категории по ID."""
        category = await self.api.get(f"{self.item_name}/{category_id}")
        return category.get("name")

