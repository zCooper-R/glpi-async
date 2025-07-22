import logging

from .api import AsyncGLPIAPI
from .cache import CacheManager
from .managers import TicketManager, CategoryManager, UserManager

logger = logging.getLogger(__name__)


class GLPIClient:
    def __init__(self, base_url: str, app_token: str, user_token: str, redis=None):
        self.api = AsyncGLPIAPI(base_url, app_token, user_token)
        self.cache = CacheManager(redis)

        self.tickets = TicketManager(self.api)
        self.categories = CategoryManager(self.api)
        self.users = UserManager(self.api)

    async def __aenter__(self):
        await self.api.init_session()
        logger.info("GLPIClient entered context")
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        await self.api.kill_session()
        await self.api.close()
        logger.info("GLPIClient exited context")

    def __repr__(self):
        return f"<GLPIClient base_url={self.api.base_url}>"
