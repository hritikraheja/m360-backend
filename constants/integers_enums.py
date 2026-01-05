from enum import Enum


class IntegersEnum(Enum):
    EXPIRY_TIME = 60 * 60
    TIME_DELTA = 3 * 100
    TTL_EXPIRATION = 30 * 24 * 60 * 60
    MAX_BYTES = 10 * 1024 * 1024
