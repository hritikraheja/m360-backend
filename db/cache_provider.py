from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheProvider(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int) -> bool:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def clear_pattern(self, pattern: str) -> int:
        pass
