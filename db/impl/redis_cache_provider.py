import redis
import json
import os
from typing import Any, Optional

from constants.system_config import SystemConfig
from db.cache_provider import CacheProvider
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class RedisCacheProvider(CacheProvider):
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        redis_password = os.getenv("REDIS_PASSWORD", None)

        timeout = SystemConfig.REDIS_CONNECTION_TIMEOUT.value

        try:
            self.client = redis.StrictRedis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                password=redis_password,
                decode_responses=True,
                socket_connect_timeout=timeout,
                socket_timeout=timeout,
            )
            self.client.ping()
            logger.info(
                f"RedisCacheProvider initialized - connected to {redis_host}:{redis_port}"
            )
        except redis.ConnectionError as e:
            logger.error(f"Redis connection failed: {e}")
            raise ConnectionError(
                f"Failed to connect to Redis at {redis_host}:{redis_port}"
            )

    def get(self, key: str) -> Optional[Any]:
        try:
            if self.client.get(key):
                logger.debug(f"[REDIS CACHE] HIT: {key}")
                return json.loads(self.client.get(key))
            logger.debug(f"[REDIS CACHE] MISS: {key}")
            return None
        except Exception as e:
            logger.error(f"[REDIS CACHE] GET error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int) -> bool:
        try:
            serialized = json.dumps(value)
            self.client.setex(key, ttl, serialized)
            logger.debug(f"[REDIS CACHE] SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"[REDIS CACHE] SET error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        try:
            result = self.client.delete(key)
            logger.debug(f"[REDIS CACHE] DELETE: {key} (deleted: {result})")
            return result > 0
        except Exception as e:
            logger.error(f"[REDIS CACHE] DELETE error for key {key}: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        try:
            if self.client.keys(pattern):
                deleted = self.client.delete(*self.client.keys(pattern))
                logger.info(
                    f"[REDIS CACHE] Cleared {deleted} keys matching pattern: {pattern}"
                )
                return deleted
            return 0
        except Exception as e:
            logger.error(
                f"[REDIS CACHE] CLEAR_PATTERN error for pattern {pattern}: {e}"
            )
            return 0

    def exists(self, key: str) -> bool:
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"[REDIS CACHE] EXISTS error for key {key}: {e}")
            return False

    def ttl(self, key: str) -> int:
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"[REDIS CACHE] TTL error for key {key}: {e}")
            return -1

    def ping(self) -> bool:
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f"[REDIS CACHE] PING failed: {e}")
            return False
