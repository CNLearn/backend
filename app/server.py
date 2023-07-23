import uvicorn

from app.app import app
from app.settings.logging.uvicorn import uvicorn_logging_config


def development() -> None:
    """
    This runs the development server.
    """
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True, log_config=uvicorn_logging_config)


def production() -> None:
    """
    This runs the production server but it will probably be run differently.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", log_config=uvicorn_logging_config)
