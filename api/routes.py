from fastapi import APIRouter
from typing import Optional

from client.quran_api_client import QuranApiClient
from config.factory.quran_config_factory import QuranConfigFactory
from constants.api_endpoints import ApiEndpoints
from db.factory.device_repository_factory import DeviceRepositoryFactory
from utils.logger import Logger
from utils.mac_address_utils import get_mac_address, validate_mac_address

router = APIRouter()
logger = Logger().get_logger()

config = QuranConfigFactory.create()
client = QuranApiClient(config)

device_repository = DeviceRepositoryFactory.create()


@router.get(ApiEndpoints.HEALTH.value)
def health():
    logger.info("GET /health")
    return {"status": "UP"}


@router.get(ApiEndpoints.CHAPTERS.value)
def get_chapters(language: str = "en"):
    logger.info(f"GET /chapters - language")
    return client.chapters.get_chapters(language)


@router.get(ApiEndpoints.SEARCH.value)
def search(q: str, size: int = 10, page: int | None = None, language: str = "en"):
    logger.info(f"GET /search - query")
    return client.search.search(q, size=size, page=page, language=language)


@router.get(ApiEndpoints.AUDIO_CHAPTER.value)
def chapter_audio(chapter_id: int, recitation_id: int):
    logger.info(
        f"GET /audio/chapter - chapter_id: {chapter_id}, recitation_id: {recitation_id}"
    )
    return client.audio.get_chapter_recitation_audio(
        chapter_id=chapter_id, recitation_id=recitation_id
    )


@router.post(ApiEndpoints.DEVICE_REGISTER.value)
def register_device(mac_address: Optional[str] = None):
    logger.info("POST /device/register")
    if not mac_address:
        mac_address = get_mac_address()
        if not mac_address:
            logger.error("Failed to detect MAC address")
            return {"error": "Could not detect MAC address"}
    if not validate_mac_address(mac_address):
        logger.warning(f"Invalid MAC address format: {mac_address}")
        return {"error": "Invalid MAC address format"}
    device_uuid = device_repository.save_device(mac_address)
    if device_uuid:
        return {"status": "success", "uuid": device_uuid, "mac_address": mac_address}
    else:
        return {"error": "Failed to register device"}


@router.get(ApiEndpoints.DEVICES.value)
def get_all_devices():
    logger.info("GET /devices")
    devices = device_repository.get_all_devices()
    return {"count": len(devices), "devices": devices}


@router.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: int, language: str = "en"):
    logger.info(f"GET /chapters/{chapter_id} - language: {language}")
    return client.chapters.get_chapter(chapter_id, language)


@router.get("/verses/by-key/{verse_key}")
def get_verse_by_key(
    verse_key: str,
    language: str = "en",
    translations: str | None = None,
    words: bool = False,
):
    logger.info(
        f"GET /verses/by-key/{verse_key} - language: {language}, translations: {translations}"
    )
    translation_ids = list(map(int, translations.split(","))) if translations else None
    return client.verses.by_key(
        verse_key=verse_key,
        language=language,
        translations=translation_ids,
        words=words,
    )


@router.get("/device/{device_uuid}")
def get_device(device_uuid: str):
    logger.info(f"GET /device/{device_uuid}")
    device = device_repository.get_device_by_uuid(device_uuid)
    if device:
        return device
    else:
        return {"error": "Device not found"}


@router.get("/device/mac/{mac_address}")
def get_device_by_mac(mac_address: str):
    logger.info(f"GET /device/mac/{mac_address}")
    device = device_repository.get_device_by_mac(mac_address)
    if device:
        return device
    else:
        return {"error": "Device not found"}


@router.delete("/device/{device_uuid}")
def delete_device(device_uuid: str):
    logger.info(f"DELETE /device/{device_uuid}")
    success = device_repository.delete_device(device_uuid)
    if success:
        return {"status": "success", "message": f"Device {device_uuid} deleted"}
    else:
        return {"error": "Device not found or could not be deleted"}
