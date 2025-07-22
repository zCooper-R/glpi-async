from glpi_async.query.query import QueryBuilder


class BaseManager:
    def __init__(self, api, item_name):
        self.api = api
        self.item_name = item_name

    def query(self):
        return QueryBuilder(self)

    async def get_options(self):
        return await self.api.get(f"listSearchOptions/{self.item_name}")

    async def map_fields(self):
        options = await self.get_options()
        return {
            field['uid'].replace(f"{self.item_name}.", ''): field_id
            for field_id, field in options.items()
            if 'uid' in field
        }