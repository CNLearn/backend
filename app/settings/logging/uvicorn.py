"""
This module contains the dictConfig based logging for uvicorn.
"""
from typing import Any

uvicorn_logging_config: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "uvicorn": {"handlers": [], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO", "handlers": []},
        "uvicorn.access": {"handlers": [], "level": "INFO", "propagate": False},
    },
}
