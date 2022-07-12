from fastapi import APIRouter

from app.api.v1.routes import sample
from app.api.v1.routes import registration

api_router = APIRouter()
api_router.include_router(sample.router, prefix="/sample", tags=["sample"])
api_router.include_router(registration.router, prefix="/users", tags=["users"])

