import asyncio
from time import time
from functools import wraps
from config.settings import Settings


class RateLimiter:
    def __init__(self):
        self.settings = Settings()
        self.function_calls = []
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time()

            # 移除过期的时间戳
            self.function_calls = [
                ts for ts in self.function_calls
                if ts > now - self.settings.RATE_LIMIT_PERIOD]

            if len(self.function_calls) >= self.settings.RATE_LIMIT_CALLS:
                # 需要等待直到最早的请求过期
                sleep_time = self.function_calls[0] - \
                    (now - self.settings.RATE_LIMIT_PERIOD)
                if sleep_time > 0:
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
                if call > now - self.settings.RATE_LIMIT_PERIOD]

            if len(self.function_calls) >= self.settings.RATE_LIMIT_CALLS:
                # wait until the earliest call would have expired
                sleep_time = self.function_calls[0] - \
                    (now - self.settings.RATE_LIMIT_PERIOD)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                self.function_calls = self.function_calls[1:]

            self.function_calls.append(now)
            return await func(*args, **kwargs)
        return wrapper


if __name__ == "__main__":
    import asyncio

    rate_limiter = RateLimiter()

    @rate_limiter
    async def test():
        print("test")

    async def main():
        for _ in range(10):
            await test()

    asyncio.run(main())
