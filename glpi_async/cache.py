import json
import logging
import time

try:
    import aioredis
except ImportError:
    aioredis = None

logger = logging.getLogger(__name__)


class CacheBackend:
    async def get(self, key): ...
    async def set(self, key, value, ttl=None): ...
    async def invalidate(self, key): ...


class InMemoryCache(CacheBackend):
    def __init__(self):
        self.store = {}

    async def get(self, key):
        entry = self.store.get(key)
        if not entry:
            return None
        if entry["expires_at"] and time.time() > entry["expires_at"]:
            await self.invalidate(key)
            return None
        return entry["value"]

    async def set(self, key, value, ttl=None):
        self.store[key] = {
            "value": value,
            "expires_at": time.time() + ttl if ttl else None
        }

    async def invalidate(self, key):
        self.store.pop(key, None)


class RedisCache(CacheBackend):
    def __init__(self, redis):
        self.redis = redis

    async def get(self, key):
        raw = await self.redis.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key, value, ttl=None):
        data = json.dumps(value)
        if ttl:
            await self.redis.set(key, data, ex=ttl)
        else:
            await self.redis.set(key, data)

    async def invalidate(self, key):
        await self.redis.delete(key)


class CacheManager(CacheBackend):
    def __init__(self, redis=None):
        if redis and aioredis is None:
            raise RuntimeError("aioredis not installed")
        self.primary = RedisCache(redis) if redis else None
        self.fallback = InMemoryCache()

    async def get(self, key):
        if self.primary:
            try:
                result = await self.primary.get(key)
                if result is not None:
                    return result
            except Exception as e:
                logger.warning(f"Redis get failed: {e}")
        return await self.fallback.get(key)

    async def set(self, key, value, ttl=None):
        if self.primary:
            try:
                return await self.primary.set(key, value, ttl)
            except Exception as e:
                logger.warning(f"Redis set failed: {e}")
        return await self.fallback.set(key, value, ttl)

    async def invalidate(self, key):
        if self.primary:
            try:
                return await self.primary.invalidate(key)
            except Exception as e:
                logger.warning(f"Redis invalidate failed: {e}")
        return await self.fallback.invalidate(key)
