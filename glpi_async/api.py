import logging

import httpx

logger = logging.getLogger(__name__)


class AsyncGLPIAPI:
    def __init__(self, base_url: str, app_token: str, user_token: str):
        self.base_url = base_url
        self.app_token = app_token
        self.user_token = user_token
        self.session_token = None
        self.client = httpx.AsyncClient(base_url=self.base_url, headers={
            'App-Token': self.app_token,
            'Content-Type': 'application/json',
        })

    async def _request(self, method: str, path: str, **kwargs):
        try:
            logger.debug(f"Sending {method} request to {path} with {kwargs}")
            response = await self.client.request(method, path, **kwargs)
            response.raise_for_status()
            logger.debug(f"Response from {path}: {response.status_code} {response.text}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Request failed: {e.response.status_code} {e.response.text}")
            raise RuntimeError(f"Request failed: {e.response.status_code} {e.response.text}") from e

    async def init_session(self):
        headers = {'Authorization': f'user_token {self.user_token}'}
        r = await self._request("GET", "/initSession", headers=headers)
        self.session_token = r.get('session_token')
        self.client.headers['Session-Token'] = self.session_token
        logger.info("Session initialized")

    async def kill_session(self):
        if self.session_token:
            await self._request("GET", "/killSession",)
            self.client.headers.pop("Session-Token", None)
            self.session_token = None
            logger.info("Session killed")

    async def get(self, path: str, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, json: dict, **kwargs):
        return await self._request("POST", path, json=json, **kwargs)

    async def put(self, path: str, json: dict, **kwargs):
        return await self._request("PUT", path, json=json, **kwargs)

    async def delete(self, path: str):
        return await self._request("DELETE", path)

    async def close(self):
        await self.client.aclose()

