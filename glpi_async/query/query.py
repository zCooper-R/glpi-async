import datetime

from .criteria import CriteriaBuilder


class QueryBuilder:
    def __init__(self, manager):
        self.manager = manager
        self.criteria = CriteriaBuilder()
        self.display = []
        self.uid_cols = True

    def where(self, field, value, searchtype="equals", link="AND"):
        self.criteria.where(field, value, searchtype, link)
        return self

    def show(self, *fields):
        self.display.extend(fields)
        return self

    # Сахар:
    def open(self):
        return self.where(12, 2)

    def close(self):
        return self.where(12, 6)

    def for_user(self, user_id):
        return self.where(22, user_id)

    def created_after(self, dt: datetime):
        return self.where(15, dt.strftime("%Y-%m-%d"), "morethan")

    def created_before(self, dt: datetime):
        return self.where(15, dt.strftime("%Y-%m-%d"), "lessthan")

    async def get(self):
        params = self.criteria.build()
        if self.uid_cols:
            params["uid_cols"] = True
        for i, val in enumerate(self.display):
            params[f"forcedisplay[{i}]"] = val
        print(params)
        return await self.manager.api.get(f"search/{self.manager.item_name}", params=params)
