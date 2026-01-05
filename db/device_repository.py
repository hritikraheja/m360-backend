from abc import ABC, abstractmethod
from typing import Optional, Dict


class DeviceRepository(ABC):
    @abstractmethod
    def save_device(self, mac_address: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_device_by_uuid(self, device_uuid: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_device_by_mac(self, mac_address: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_devices(self) -> list:
        pass

    @abstractmethod
    def delete_device(self, device_uuid: str) -> bool:
        pass
