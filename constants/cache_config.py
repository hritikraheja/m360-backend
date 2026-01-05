from enum import Enum


class CacheConfig(Enum):
    TTL_EXPIRATION = 30 * 24 * 60 * 60
    DEFAULT_EXPIRY = 60 * 60
