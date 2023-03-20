from src.config import SETTINGS

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "ch_formatter": {
            "format": "%(asctime)s - %(levelname)s - %(message)s - %(name)s"
        },
        "ph_formatter": {
            "format": "%(levelname)s - %(message)s - %(name)s - line number:%(lineno)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "ch_formatter",
        },
        "papertrail": {
            "class": "logging.handlers.SysLogHandler",
            "level": "DEBUG",
            "address": (SETTINGS.papertrail_host, SETTINGS.papertrail_port),
            "formatter": "ph_formatter",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "papertrail"
        ]
    }
}
