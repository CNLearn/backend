from fastapi import APIRouter

from app.features.auth import auth_router
from app.features.vocabulary import vocabulary_router

api_router = APIRouter()
api_router.include_router(vocabulary_router, prefix="/vocabulary", tags=["vocabulary"])
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
