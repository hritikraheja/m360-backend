import uuid
import re
from typing import Optional

from utils.logger import Logger

logger = Logger.get_logger(__name__)


def get_mac_address() -> Optional[str]:
    try:
        mac = uuid.getnode()
        mac_address = ":".join(re.findall("..", "%012x" % mac))
        logger.info(f"Retrieved MAC address: {mac_address}")
        return mac_address
    except Exception as e:
        logger.error(f"Error getting MAC address: {e}")
        return None


def validate_mac_address(mac: str) -> bool:
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return bool(re.match(pattern, mac))
