"""
Custom exceptions for the Web3 Gateway service.

This module defines the custom exceptions used throughout the application
for handling specific error cases related to caching and rate limiting.
"""


class CacheException(Exception):
    """
    Exception raised for cache-related errors.

    This exception is raised when there are issues with the caching service,
    such as connection failures, invalid cache operations, or cache corruption.

    Example:
        try:
            cache.set(key, value)
        except CacheException as e:
            logger.error(f"Cache operation failed: {str(e)}")
    """
    pass


class RateLimitException(Exception):
    """
    Exception raised when rate limits are exceeded.

    This exception is raised when API rate limits are exceeded,
    either for external services (like Etherscan) or internal API endpoints.

    Attributes:
        retry_after (int): Seconds to wait before retrying (optional)

    Example:
        if requests_count > RATE_LIMIT:
            raise RateLimitException("Rate limit exceeded. Try again later.")
    """
    pass
