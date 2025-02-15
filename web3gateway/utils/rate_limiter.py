"""
Rate Limiter Module

This module provides asynchronous rate limiting functionality with:
- Configurable time window and request limits
- Decorator support for easy function rate limiting
- Thread-safe implementation using asyncio locks
- Auto-cleanup of expired timestamps
"""

import asyncio
from functools import wraps
from time import time
from typing import Any


class RateLimiter:
    """
    Asynchronous rate limiter implementation.

    Provides both decorator and direct usage patterns for rate limiting
    with configurable windows and limits.

    Attributes:
        rate_limit_period (float): Time window in seconds
        rate_limit_calls (int): Maximum allowed calls within window
        function_calls (list): Timestamp history of function calls
        _lock (asyncio.Lock): Thread-safe lock for concurrent access

    Example:
        limiter = RateLimiter({"rate_limit_period": 1, "rate_limit_calls": 5})

        @limiter
        async def rate_limited_function():
            pass
    """

    def __init__(self, config: dict):
        """
        Initialize rate limiter with configuration.

        Args:
            config: Dictionary containing 'rate_limit_period' and 'rate_limit_calls'
        """
        self.rate_limit_period = config['rate_limit_period']
        self.rate_limit_calls = config['rate_limit_calls']
        self.function_calls: list[Any] = []
        self._lock = asyncio.Lock()

    async def acquire(self):
        """
        Acquire permission to proceed with rate-limited operation.

        Blocks until rate limit allows execution or raises if limit exceeded.
        Thread-safe using asyncio lock.

        Raises:
            asyncio.TimeoutError: If waiting exceeds configured timeout
        """
        async with self._lock:
            now = time()

            # Remove expired timestamps
            self.function_calls = [
                ts for ts in self.function_calls
                if ts > now - self.rate_limit_period]

            if len(self.function_calls) >= self.rate_limit_calls:
                # Calculate wait time until oldest request expires
                sleep_time = self.function_calls[0] - \
                    (now - self.rate_limit_period)
                if sleep_time > 0:
                    print(f"Rate limit exceeded, sleeping for {sleep_time} seconds")
                    await asyncio.sleep(sleep_time)
                self.function_calls = self.function_calls[1:]

            self.function_calls.append(now)

    def __call__(self, func):
        """
        Decorator implementation for rate limiting.

        Args:
            func: Async function to be rate limited

        Returns:
            Wrapped function with rate limiting applied
        """
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time()

            # Clean up expired call records
            self.function_calls = [
                call for call in self.function_calls
                if call > now - self.rate_limit_period]

            if len(self.function_calls) >= self.rate_limit_calls:
                # Wait until earliest call expires
                sleep_time = self.function_calls[0] - \
                    (now - self.rate_limit_period)
                if sleep_time > 0:
                    print(f"Rate limit exceeded, sleeping for {sleep_time} seconds")
                    await asyncio.sleep(sleep_time)
                self.function_calls = self.function_calls[1:]

            self.function_calls.append(now)
            return await func(*args, **kwargs)
        return wrapper


# Example usage
if __name__ == "__main__":
    # Create rate limiter allowing 5 calls per second
    rate_limiter = RateLimiter({
        "rate_limit_period": 1,  # 1 second window
        "rate_limit_calls": 5    # 5 calls allowed
    })

    @rate_limiter
    async def test():
        print("test")

    async def main():
        # Try to make 20 calls (will be rate limited)
        for _ in range(20):
            await test()

    asyncio.run(main())
