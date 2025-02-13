import asyncio
from functools import wraps
from time import time
from typing import Any


class RateLimiter:
    def __init__(self, config: dict):
        self.rate_limit_period = config['rate_limit_period']
        self.rate_limit_calls = config['rate_limit_calls']
        self.function_calls: list[Any] = []
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time()

            # 移除过期的时间戳
            self.function_calls = [
                ts for ts in self.function_calls
                if ts > now - self.rate_limit_period]

            if len(self.function_calls) >= self.rate_limit_calls:
                # 需要等待直到最早的请求过期
                sleep_time = self.function_calls[0] - \
                    (now - self.rate_limit_period)
                if sleep_time > 0:
                    print(f"Rate limit exceeded, sleeping for {sleep_time} seconds")
                    await asyncio.sleep(sleep_time)
                self.function_calls = self.function_calls[1:]

            self.function_calls.append(now)

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time()

            # 清理过期的调用记录
            self.function_calls = [
                call for call in self.function_calls
                if call > now - self.rate_limit_period]

            if len(self.function_calls) >= self.rate_limit_calls:
                # wait until the earliest call would have expired
                sleep_time = self.function_calls[0] - \
                    (now - self.rate_limit_period)
                if sleep_time > 0:
                    print(f"Rate limit exceeded, sleeping for {sleep_time} seconds")
                    await asyncio.sleep(sleep_time)
                self.function_calls = self.function_calls[1:]

            self.function_calls.append(now)
            return await func(*args, **kwargs)
        return wrapper


if __name__ == "__main__":
    rate_limiter = RateLimiter({
        "rate_limit_period": 1,
        "rate_limit_calls": 5
    })

    @rate_limiter
    async def test():
        print("test")

    async def main():
        for _ in range(20):
            await test()

    asyncio.run(main())
