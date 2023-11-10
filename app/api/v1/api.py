from fastapi import APIRouter

from app.api.v1.routes import authentication, registration, vocabulary

api_router = APIRouter()
api_router.include_router(vocabulary.router, prefix="/vocabulary", tags=["vocabulary"])
api_router.include_router(registration.router, prefix="/users", tags=["users"])
api_router.include_router(authentication.router, tags=["authentication"])
