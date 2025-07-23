from .base import BaseManager


class CategoryManager(BaseManager):
    def __init__(self, api):
        super().__init__(api, 'ITILCategory')

    async def list(self):
        return await self.api.get(f"{self.item_name}")

    async def get_name(self, category_id: int) -> str:
        category = await self.api.get(f"{self.item_name}/{category_id}")
        return category["name"]

    async def list_sorted_by_name(self):
        params = {
            "uid_cols": True,
            "order": "ASC",

        }
        result = await self.api.get(f"/search/{self.item_name}", params=params)
        return result["data"]