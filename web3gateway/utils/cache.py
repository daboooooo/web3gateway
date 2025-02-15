"""
Redis Cache Service Module

This module provides a wrapper around Redis for caching operations with:
- JSON serialization/deserialization
- Error handling and custom exceptions
- Prefix-based cache management
- Asynchronous operations
"""

import json
from typing import Any, Optional

from redis.asyncio import Redis  # type: ignore

from web3gateway.exceptions import CacheException


class CacheService:
    """
    Asynchronous Redis cache service with JSON serialization.

    This class provides a high-level interface for cache operations with automatic
    JSON serialization and comprehensive error handling.

    Attributes:
        redis: Async Redis client instance
        _connected: Connection status flag

    Example:
        cache = CacheService("redis://localhost:6379/0")
        await cache.initialize()
        await cache.set("key", {"value": 123}, expire=300)
    """

    def __init__(self, redis_url: str):
        """
        Initialize cache service with Redis connection URL.

        Args:
            redis_url: Redis connection string (e.g., "redis://localhost:6379/0")

        Raises:
            CacheException: If Redis connection fails
        """
        try:
            self.redis = Redis.from_url(redis_url, decode_responses=True)
            self._connected = False
        except Exception as e:
            raise CacheException(f"Redis connection failed: {str(e)}") from e

    async def initialize(self) -> None:
        """
        Initialize Redis connection with ping check.

        Raises:
            CacheException: If Redis ping fails
        """
        try:
            self._connected = await self.redis.ping()
        except Exception as e:
            raise CacheException(f"Redis initialization failed: {str(e)}") from e

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve and deserialize a value from cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Optional[Any]: Deserialized value or None if not found

        Raises:
            CacheException: If retrieval or deserialization fails
        """
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except json.JSONDecodeError as e:
            # Auto-cleanup corrupted cache entries
            await self.delete(key)
            raise CacheException(f"Cache value decode error for key: {key}") from e
        except Exception as e:
            raise CacheException(f"Cache get error: {str(e)}") from e

    async def set(self, key: str, value: Any, expire: int = 0) -> bool:
        """
        Serialize and store a value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            expire: Expiration time in seconds (0 for no expiration)

        Returns:
            bool: True if successful

        Raises:
            CacheException: If serialization or storage fails
        """
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
        """
        Delete a key from cache.

        Args:
            key: Cache key to delete

        Returns:
            bool: True if key was deleted

        Raises:
            CacheException: If deletion fails
        """
        try:
            return await self.redis.delete(key) > 0
        except Exception as e:
            raise CacheException(f"Cache delete error: {str(e)}") from e

    async def clear_prefix(self, prefix: str) -> int:
        """
        Delete all keys matching a prefix pattern.

        Args:
            prefix: Key prefix to match for deletion

        Returns:
            int: Number of keys deleted

        Raises:
            CacheException: If clearing fails
        """
        try:
            cursor = 0
            deleted_count = 0
            while True:
                # Scan for matching keys in batches
                cursor, keys = await self.redis.scan(cursor, f"{prefix}*")
                if keys:
                    deleted_count += await self.redis.delete(*keys)
                if cursor == 0:
                    break
            return deleted_count
        except Exception as e:
            raise CacheException(f"Cache clear error: {str(e)}") from e
