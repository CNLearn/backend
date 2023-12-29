import uvicorn

from app.app import create_application
from app.settings.logging.uvicorn import uvicorn_logging_config


def development() -> None:
    """
    This runs the development server.
    """
    uvicorn.run(
        "app.app:create_application",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_config=uvicorn_logging_config,
        factory=True,
    )


def production() -> None:
    """
    This runs the production server but it will probably be run differently.
    """
    uvicorn.run(
        create_application,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        log_config=uvicorn_logging_config,
        factory=True,
    )
