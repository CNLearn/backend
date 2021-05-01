from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router


def create_application():
    """
    Creates and returns a FastAPI instance.
    """
    app = FastAPI(
        title="Web CNLearn Backend",  # TODO: retrieve this from settings
        version="0.0.5"  # TODO: retrieve this from settings
    )
    # change CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: retrieve this from settings
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app


app = create_application()
