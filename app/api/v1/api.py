from fastapi import APIRouter

from app.api.v1.routes import sample

api_router = APIRouter()
api_router.include_router(sample.router, prefix="/sample", tags=["sample"])
