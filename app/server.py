from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.settings.base import settings
from app.tasks.startup import database_start_app_handler
from app.tasks.shutdown import database_stop_app_handler


def create_application():
    """
    Creates and returns a FastAPI instance.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
    )
    app.add_event_handler("startup", database_start_app_handler(app))
    app.add_event_handler("shutdown", database_stop_app_handler(app))
    # change CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app


app = create_application()
