"""Logging module."""
import logging
from logging.config import dictConfig


# Configure logging
def setup_logging():
    """Set up logging configuration."""
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }
    dictConfig(log_config)


# Set up logging
setup_logging()
logging = logging.getLogger(__name__)
