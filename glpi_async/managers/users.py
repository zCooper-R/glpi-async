from .base import BaseManager


class UserManager(BaseManager):
    def __init__(self, api):
        super().__init__(api, 'User')

    async def get_my_id(self) -> int:
        r = await self.api.get("getFullSession/")
        return r.get('session').get('glpiID')

    async def get(self, user_id: int):
        return await self.api.get(f"{self.item_name}/{user_id}")

    async def get_name(self, user_id: int) -> str:
        user = await self.get(user_id)
        return user.get("realname", "") + " " + user.get("firstname", "")
