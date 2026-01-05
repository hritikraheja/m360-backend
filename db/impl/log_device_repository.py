import uuid
from typing import Optional, Dict
from db.device_repository import DeviceRepository
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class LogDeviceRepository(DeviceRepository):

    def __init__(self):
        self.devices_by_mac = {}
        self.devices_by_uuid = {}
        logger.info(
            "LogDeviceRepository initialized - using in-memory storage with logging"
        )

    def save_device(self, mac_address: str) -> Optional[str]:
        try:
            if mac_address in self.devices_by_mac:
                device_uuid = self.devices_by_mac[mac_address]
                logger.info(
                    f"[LOG REPOSITORY] Device already exists: UUID={device_uuid}, MAC={mac_address}"
                )
                return device_uuid

            device_uuid = str(uuid.uuid4())
            self.devices_by_mac[mac_address] = device_uuid
            self.devices_by_uuid[device_uuid] = mac_address

            logger.info(
                f"[LOG REPOSITORY] New device registered: UUID={device_uuid}, MAC={mac_address}"
            )
            logger.warning(
                f"[PREPROD MODE] Device NOT saved to database, only logged. UUID={device_uuid}"
            )

            return device_uuid

        except Exception as e:
            logger.error(f"[LOG REPOSITORY] Error saving device: {e}")
            return None

    def get_device_by_uuid(self, device_uuid: str) -> Optional[Dict]:
        try:
            if device_uuid in self.devices_by_uuid:
                mac_address = self.devices_by_uuid[device_uuid]
                result = {"uuid": device_uuid, "mac_address": mac_address}
                logger.info(f"[LOG REPOSITORY] Device found by UUID: {result}")
                return result

            logger.info(f"[LOG REPOSITORY] Device not found for UUID: {device_uuid}")
            return None

        except Exception as e:
            logger.error(f"[LOG REPOSITORY] Error getting device by UUID: {e}")
            return None

    def get_device_by_mac(self, mac_address: str) -> Optional[Dict]:
        try:
            if mac_address in self.devices_by_mac:
                device_uuid = self.devices_by_mac[mac_address]
                result = {"uuid": device_uuid, "mac_address": mac_address}
                return result

            logger.info(f"[LOG REPOSITORY] Device not found for MAC: {mac_address}")
            return None

        except Exception as e:
            logger.error(f"[LOG REPOSITORY] Error getting device by MAC: {e}")
            return None

    def get_all_devices(self) -> list:
        try:
            devices = [
                {"uuid": uuid_val, "mac_address": mac}
                for mac, uuid_val in self.devices_by_mac.items()
            ]
            logger.info(f"[LOG REPOSITORY] Retrieved {len(devices)} devices")
            return devices

        except Exception as e:
            logger.error(f"[LOG REPOSITORY] Error getting all devices: {e}")
            return []

    def delete_device(self, device_uuid: str) -> bool:
        try:
            if device_uuid in self.devices_by_uuid:
                mac_address = self.devices_by_uuid[device_uuid]
                del self.devices_by_uuid[device_uuid]
                del self.devices_by_mac[mac_address]
                logger.info(
                    f"[LOG REPOSITORY] Device deleted: UUID={device_uuid}, MAC={mac_address}"
                )
                return True

            logger.info(
                f"[LOG REPOSITORY] Device not found for deletion: UUID={device_uuid}"
            )
            return False

        except Exception as e:
            logger.error(f"[LOG REPOSITORY] Error deleting device: {e}")
            return False

    def count_devices(self) -> int:
        return len(self.devices_by_mac)
