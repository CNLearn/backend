from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import v1
from app.core.exceptions import CNLearnWithMessage
from app.core.handlers import cnlearn_exception_handler
from app.middleware.logger import AccessLogger
from app.settings.base import app_settings
from app.settings.logging.structlog import configure_logging
from app.state import lifespan


def create_application() -> FastAPI:
    """
    Creates and returns a FastAPI instance.
    """
    app = FastAPI(
        title=app_settings.APP_NAME,
        version=app_settings.VERSION,
        lifespan=lifespan,
    )
    logger = configure_logging()
    # change CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AccessLogger, logger=logger)
    app.include_router(v1.api_router, prefix=app_settings.API_V1_STR)
    app.add_exception_handler(CNLearnWithMessage, cnlearn_exception_handler)  # pyright: ignore[reportUnknownMemberType]
    return app


app: FastAPI = create_application()
