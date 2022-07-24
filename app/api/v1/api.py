from fastapi import APIRouter

from app.api.v1.routes import registration, sample

api_router = APIRouter()
api_router.include_router(sample.router, prefix="/sample", tags=["sample"])
api_router.include_router(registration.router, prefix="/users", tags=["users"])
