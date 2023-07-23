"""
This module contains the logging settings for both the uvicorn server
as well as the structlog configuration that's used in both the FastAPI
logging middleware and separate loggers for the various modules.
"""
import logging

import orjson
import structlog
from structlog.typing import Processor

from app.settings.base import settings


def configure_logging() -> structlog.BoundLogger:
    common_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
    ]
    logging.basicConfig(
        format="%(message)s",
    )
    if settings.ENVIRONMENT == "Development":
        logging.getLogger().setLevel(logging.DEBUG)
        structlog.configure(
            processors=common_processors
            + [
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
            cache_logger_on_first_use=False,
        )
    else:
        logging.getLogger().setLevel(logging.INFO)
        structlog.configure(
            processors=common_processors
            + [
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(serializer=orjson.dumps),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            context_class=dict,
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            cache_logger_on_first_use=False,
        )

    log: structlog.BoundLogger = structlog.get_logger()
    log.info("Starting logging")

    return log
