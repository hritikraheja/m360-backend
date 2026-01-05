from abc import ABC, abstractmethod
from typing import Dict, Any


class HttpClient(ABC):

    @abstractmethod
    def get(self, url: str, headers: Dict[str, str], params: Dict[str, Any]) -> Dict:
        pass
