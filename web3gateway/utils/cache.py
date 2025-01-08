from redis.asyncio import Redis
from typing import Optional, Any, Dict, List
import json
import logging
# import asyncio
# 修改为相对导入
from .exceptions import CacheException
from .metrics import metrics_service
# from .blockchain import blockchain_service

class CacheService:
    def __init__(self, redis_url: str):
        try:
            self.redis = Redis.from_url(redis_url, decode_responses=True)
            self._connected = False
            self.metrics = metrics_service
        except Exception as e:
            raise CacheException(f"Redis connection failed: {str(e)}")

    async def initialize(self):
        """初始化缓存服务"""
        try:
            self._connected = await self.redis.ping()
        except Exception as e:
            raise CacheException(f"Redis initialization failed: {str(e)}")

    async def get(self, key: str, cache_type: str = 'default') -> Optional[Any]:
        try:
            value = await self.redis.get(key)
            if value:
                self.metrics.cache_hits.labels(cache_type=cache_type).inc()
                return json.loads(value)
            self.metrics.cache_misses.labels(cache_type=cache_type).inc()
            return None
        except json.JSONDecodeError:
            logging.error(f"Cache value decode error for key: {key}")
            await self.delete(key)
            return None
        except Exception as e:
            self.metrics.error_counter.labels(
                error_type='cache_error',
                chain_id='all'
            ).inc()
            raise CacheException(f"Cache get error: {str(e)}")

    async def set(self, key: str, value: Any, expire: int = None) -> bool:
        try:
            serialized = json.dumps(value)
            if expire:
                return await self.redis.set(key, serialized, ex=expire)
            return await self.redis.set(key, serialized)
        except (TypeError, ValueError) as e:
            raise CacheException(f"Cache serialization error: {str(e)}")
        except Exception as e:
            raise CacheException(f"Cache set error: {str(e)}")

    async def delete(self, key: str) -> bool:
        try:
            return await self.redis.delete(key) > 0
        except Exception as e:
            raise CacheException(f"Cache delete error: {str(e)}")

    async def clear_prefix(self, prefix: str) -> int:
        """清除指定前缀的所有缓存"""
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
            raise CacheException(f"Cache clear error: {str(e)}")

    # async def warm_up(self, chain_id: str, addresses: List[str]):
    #     """缓存预热机制"""
    #     try:
    #         # 批量获取地址余额
    #         tasks = []
    #         for address in addresses:
    #             tasks.append(self._warm_up_address(chain_id, address))
    #         await asyncio.gather(*tasks)
    #     except Exception as e:
    #         logging.error(f"Cache warm up failed: {str(e)}")
            
    # async def _warm_up_address(self, chain_id: str, address: str):
    #     """预热单个地址的相关数据"""
    #     try:
    #         # 获取基础数据
    #         balance = await blockchain_service.get_balance(chain_id, address)
    #         await self.set(f"balance:{chain_id}:{address}", balance, expire=300)
            
    #         # 获取代币数据
    #         tokens = await blockchain_service.get_tokens(chain_id, address)
    #         await self.set(f"tokens:{chain_id}:{address}", tokens, expire=300)
            
    #         # 获取最近交易
    #         txs = await blockchain_service.get_transactions(chain_id, address)
    #         await self.set(f"transactions:{chain_id}:{address}", txs, expire=300)
    #     except Exception as e:
    #         logging.error(f"Failed to warm up data for {address}: {str(e)}")
