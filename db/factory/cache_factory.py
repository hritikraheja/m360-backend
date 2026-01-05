import os

from constants.environment import Environment
from db.cache_provider import CacheProvider
from db.impl.local_cache_provider import LocalCacheProvider
from db.impl.redis_cache_provider import RedisCacheProvider
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class CacheFactory:
    _cache_instance = None

    @staticmethod
    def create() -> CacheProvider:
        if CacheFactory._cache_instance is not None:
            return CacheFactory._cache_instance

        env = os.getenv("APP_ENV", Environment.PREPROD.value).lower()

        if env in [
            Environment.PREPROD.value,
            Environment.DEV.value,
            Environment.LOCAL.value,
        ]:
            logger.info(f"Creating LocalCacheProvider for {env} environment")
            CacheFactory._cache_instance = LocalCacheProvider()
        elif env == Environment.PROD.value:
            logger.info("Creating RedisCacheProvider for prod environment")
            try:
                CacheFactory._cache_instance = RedisCacheProvider()
            except ConnectionError as e:
                logger.error(f"Failed to create RedisCacheProvider: {e}")
                CacheFactory._cache_instance = LocalCacheProvider()
        else:
            logger.warning(
                f"Unknown environment '{env}', defaulting to LocalCacheProvider"
            )
            CacheFactory._cache_instance = LocalCacheProvider()

        return CacheFactory._cache_instance

    @staticmethod
    def reset():
        CacheFactory._cache_instance = None
