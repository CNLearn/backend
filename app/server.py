import uvicorn

from app.app import app


def development() -> None:
    """
    This runs the development server.
    """
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)


def production() -> None:
    """
    This runs the production server but it will probably be run differently.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
