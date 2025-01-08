import os


class Settings:

    # 项目配置
    INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

    # 数据库配置
    REDIS_URL = os.getenv("REDIS_URL")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

    # API限流配置
    RATE_LIMIT_CALLS = 5  # 每秒最大请求数
    RATE_LIMIT_PERIOD = 1  # 限流周期(秒)

    # 缓存配置
    CACHE_EXPIRATION = 10  # 缓存有效期(秒)
