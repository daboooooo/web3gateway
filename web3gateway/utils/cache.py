import json
from typing import Any, Optional

from redis.asyncio import Redis  # type: ignore

from web3gateway.exceptions import CacheException


class CacheService:
    def __init__(self, redis_url: str):
        try:
            self.redis = Redis.from_url(redis_url, decode_responses=True)
            self._connected = False
        except Exception as e:
            raise CacheException(f"Redis connection failed: {str(e)}") from e

    async def initialize(self):
        """ initialize the cache service """
        try:
            self._connected = await self.redis.ping()
        except Exception as e:
            raise CacheException(f"Redis initialization failed: {str(e)}") from e

    async def get(self, key: str) -> Optional[Any]:
        """ get a value from the cache """
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except json.JSONDecodeError as e:
            await self.delete(key)
            raise CacheException(f"Cache value decode error for key: {key}") from e
        except Exception as e:
            raise CacheException(f"Cache get error: {str(e)}") from e

    async def set(self, key: str, value: Any, expire: int = 0) -> bool:
        """ set a value in the cache """
        try:
            serialized = json.dumps(value)
            if expire != 0:
                result = await self.redis.set(key, serialized, ex=expire)
                if not result:
                    raise CacheException(f"Cache set error: {key}")
                return result
            result = await self.redis.set(key, serialized)
            if not result:
                raise CacheException(f"Cache set error: {key}")
            return result
        except (TypeError, ValueError) as e:
            raise CacheException(f"Cache serialization error: {str(e)}") from e
        except Exception as e:
            raise CacheException(f"Cache set error: {str(e)}") from e

    async def delete(self, key: str) -> bool:
        """ delete a key from the cache """
        try:
            return await self.redis.delete(key) > 0
        except Exception as e:
            raise CacheException(f"Cache delete error: {str(e)}") from e

    async def clear_prefix(self, prefix: str) -> int:
        """ clear all keys with the given prefix """
        try:
            cursor = 0
            deleted_count = 0
            while True:
                cursor, keys = await self.redis.scan(cursor, f"{prefix}*")
                if keys:
                    deleted_count += await self.redis.delete(*keys)
                if cursor == 0:
                    break
            return deleted_count
        except Exception as e:
            raise CacheException(f"Cache clear error: {str(e)}") from e
