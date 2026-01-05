import os

from constants.environment import Environment
from db.device_repository import DeviceRepository
from db.impl.log_device_repository import LogDeviceRepository
from db.impl.mongo_device_repository import MongoDeviceRepository
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class DeviceRepositoryFactory:
    _repository_instance = None

    @staticmethod
    def create() -> DeviceRepository:
        if DeviceRepositoryFactory._repository_instance is not None:
            return DeviceRepositoryFactory._repository_instance

        env = os.getenv("APP_ENV", Environment.PREPROD.value).lower()

        if env in [
            Environment.PREPROD.value,
            Environment.DEV.value,
            Environment.LOCAL.value,
        ]:
            logger.info(f"Creating LogDeviceRepository for {env} environment")
            DeviceRepositoryFactory._repository_instance = LogDeviceRepository()
        elif env == Environment.PROD.value:
            logger.info("Creating MongoDeviceRepository for prod environment")
            try:
                DeviceRepositoryFactory._repository_instance = MongoDeviceRepository()
            except ConnectionError as e:
                logger.error(f"Failed to create MongoDeviceRepository: {e}")
                DeviceRepositoryFactory._repository_instance = LogDeviceRepository()
        else:
            logger.warning(
                f"Unknown environment '{env}', defaulting to LogDeviceRepository"
            )
            DeviceRepositoryFactory._repository_instance = LogDeviceRepository()

        return DeviceRepositoryFactory._repository_instance

    @staticmethod
    def reset():
        DeviceRepositoryFactory._repository_instance = None
