import uuid
import os
from typing import Optional, Dict
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

from constants.system_config import SystemConfig
from db.device_repository import DeviceRepository
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class MongoDeviceRepository(DeviceRepository):
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        mongo_db = os.getenv("MONGO_DB", "quran_api")

        try:
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=int(
                    SystemConfig.MONGO_CONNECTION_TIMEOUT.value
                ),
                connectTimeoutMS=int(SystemConfig.MONGO_CONNECTION_TIMEOUT.value),
            )
            self.client.admin.command("ping")
            self.db = self.client[mongo_db]
            self.devices_collection = self.db["devices"]

            self.devices_collection.create_index("mac_address", unique=True)
            self.devices_collection.create_index("uuid", unique=True)

            logger.info(f"MongoDeviceRepository initialized - connected to {mongo_db}")

        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise ConnectionError(f"Failed to connect to MongoDB at {mongo_uri}")

    def save_device(self, mac_address: str) -> Optional[str]:
        try:
            existing = self.devices_collection.find_one({"mac_address": mac_address})
            if existing:
                logger.info(
                    f"[MONGO REPOSITORY] Device already exists: UUID={existing['uuid']}, MAC={mac_address}"
                )
                return existing["uuid"]

            device_uuid = str(uuid.uuid4())
            document = {"uuid": device_uuid, "mac_address": mac_address}

            self.devices_collection.insert_one(document)
            logger.info(
                f"[MONGO REPOSITORY] New device saved: UUID={device_uuid}, MAC={mac_address}"
            )
            return device_uuid

        except DuplicateKeyError:
            existing = self.devices_collection.find_one({"mac_address": mac_address})
            if existing:
                logger.info(
                    f"[MONGO REPOSITORY] Device found after race condition: UUID={existing['uuid']}"
                )
                return existing["uuid"]
            return None

        except Exception as e:
            logger.error(f"[MONGO REPOSITORY] Error saving device: {e}")
            return None

    def get_device_by_uuid(self, device_uuid: str) -> Optional[Dict]:
        try:
            device = self.devices_collection.find_one({"uuid": device_uuid}, {"_id": 0})

            if device:
                logger.info(f"[MONGO REPOSITORY] Device found by UUID: {device}")
            else:
                logger.info(
                    f"[MONGO REPOSITORY] Device not found for UUID: {device_uuid}"
                )

            return device

        except Exception as e:
            logger.error(f"[MONGO REPOSITORY] Error getting device by UUID: {e}")
            return None

    def get_device_by_mac(self, mac_address: str) -> Optional[Dict]:
        try:
            device = self.devices_collection.find_one(
                {"mac_address": mac_address}, {"_id": 0}
            )

            if device:
                logger.info(f"[MONGO REPOSITORY] Device found by MAC: {device}")
            else:
                logger.info(
                    f"[MONGO REPOSITORY] Device not found for MAC: {mac_address}"
                )

            return device

        except Exception as e:
            logger.error(f"[MONGO REPOSITORY] Error getting device by MAC: {e}")
            return None

    def get_all_devices(self) -> list:
        try:
            devices = list(self.devices_collection.find({}, {"_id": 0}))
            logger.info(f"[MONGO REPOSITORY] Retrieved {len(devices)} devices")
            return devices

        except Exception as e:
            logger.error(f"[MONGO REPOSITORY] Error getting all devices: {e}")
            return []

    def delete_device(self, device_uuid: str) -> bool:
        try:
            result = self.devices_collection.delete_one({"uuid": device_uuid})

            if result.deleted_count > 0:
                logger.info(f"[MONGO REPOSITORY] Device deleted: UUID={device_uuid}")
                return True

            logger.info(
                f"[MONGO REPOSITORY] Device not found for deletion: UUID={device_uuid}"
            )
            return False

        except Exception as e:
            logger.error(f"[MONGO REPOSITORY] Error deleting device: {e}")
            return False

    def count_devices(self) -> int:
        try:
            return self.devices_collection.count_documents({})
        except Exception as e:
            logger.error(f"[MONGO REPOSITORY] Error counting devices: {e}")
            return 0

    def ping(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except Exception as e:
            logger.error(f"[MONGO REPOSITORY] PING failed: {e}")
            return False
