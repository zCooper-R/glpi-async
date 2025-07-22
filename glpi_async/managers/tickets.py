from __future__ import annotations

from datetime import datetime

import aiohttp

from .base import BaseManager


class TicketStatus:
    UID = 12

    STATUS_OPEN = 2


class TicketManager(BaseManager):
    def __init__(self, api, cache=None):
        super().__init__(api, 'Ticket')
        self.cache = cache

    @staticmethod
    def build_ticket_payload(name, content, category_id, request_source_id, time_to_resolve=None):
        payload = {
            "input": {
                "name": name,
                "content": content,
                "status": TicketStatus.STATUS_OPEN,
                "itilcategories_id": category_id,
                "requesttypes_id": request_source_id,
            }
        }
        if time_to_resolve:
            payload['input']["time_to_resolve"] = time_to_resolve.isoformat(timespec="minutes")
        return payload

    async def upload_file(
        self,
        ticket_id: int,
        file_bytes: bytes,
        filename: str,
        mime_type: str = "image/png"
    ):
        form = aiohttp.FormData()
        form.add_field("uploadManifest", "1")
        form.add_field("filename", file_bytes, filename=filename, content_type=mime_type)

        document = await self.api.post("/Document", data=form)

        await self.api.post("/Document_Item", json={
            "input": {
                "documents_id": document["id"],
                "itemtype": "Ticket",
                "items_id": ticket_id
            }
        })

        return document


    async def list(self, params=None):
        return await self.api.get(f"{self.item_name}", params=params)

    async def get(self, ticket_id: int):
        return await self.api.get(f"{self.item_name}/{ticket_id}")

    async def update(self, ticket_id: int, data: dict):
        return await self.api.put(f"{self.item_name}/{ticket_id}", json=data)

    async def delete(self, ticket_id: int):
        return await self.api.delete(f"{self.item_name}/{ticket_id}")

    async def create(
            self,
            name: str,
            content: str,
            category_id: int,
            request_source_id: int = None,
            time_to_resolve: datetime | None = None
    ):
        data = TicketManager.build_ticket_payload(name, content, category_id, request_source_id, time_to_resolve)
        return await self.api.post(f"{self.item_name}", json=data)

    async def list_open(self):

        return await self.api.get(
            f"search/{self.item_name}",
            params={
                "uid_cols": True,
                "criteria[0][field]": "12",
                "criteria[0][searchtype]": "equals",
                "criteria[0][value]": TicketStatus.STATUS_OPEN,
            }
        )

    async def list_open_for_user(self, user_id: int):
        cache_key = f"glpi:tickets:open:user:{user_id}"
        if self.cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        result = await self.api.get(
            f"search/{self.item_name}",
            params={
                'uid_cols': True,
                "criteria[0][field]": "12",
                "criteria[0][searchtype]": "equals",
                "criteria[0][value]": TicketStatus.STATUS_OPEN,
                "criteria[1][link]": "AND",
                "criteria[1][field]": "22",
                "criteria[1][searchtype]": "equals",
                "criteria[1][value]": user_id,

            }
        )
        if self.cache:
            await self.cache.set(cache_key, result, ttl=300)
        return result


