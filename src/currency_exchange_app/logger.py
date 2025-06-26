import logging.config
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple_format": {
            "format": "{asctime} - {levelname} - {module}:{lineno} - {message}",
            "style": "{",
            "datefmt": "%H:%M:%S",
        },
        "color_format": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s - %(levelname)s - %(module)s:%(lineno)s - %(message)s",
            "datefmt": "%H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "color_format",
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": LOG_DIR / "debug.log",
            "formatter": "simple_format",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 1,
            "encoding": "utf8",
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": LOG_DIR / "error.log",
            "formatter": "simple_format",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 1,
            "encoding": "utf8",
        },
    },
    "loggers": {
        #     "currency_exchange": {
        #         "level": "DEBUG",
        #         "handlers": ["console", "debug_file_handler", "error_file_handler"],
        #         "propagate": False,
        #     },
        "currency_exchange_app": {
            "level": "DEBUG",
            "handlers": ["console", "debug_file_handler", "error_file_handler"],
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("currency_exchange_app")
