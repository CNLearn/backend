from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.settings.base import settings
from app.state import lifespan


def create_application() -> FastAPI:
    """
    Creates and returns a FastAPI instance.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )
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


app: FastAPI = create_application()
