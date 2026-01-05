import logging
import sys
import os
from logging.handlers import RotatingFileHandler

from constants.system_config import SystemConfig


class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, name: str = "QuranAPI") -> logging.Logger:
        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if logger.handlers:
            return logger

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        os.makedirs("logs", exist_ok=True)
        file_handler = RotatingFileHandler(
            "logs/quran_api.log",
            maxBytes=SystemConfig.MAX_BYTES.value,
            backupCount=5,
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s "
            "- [%(filename)s:%(lineno)d] - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        cls._logger = logger
        return logger
