from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain.auth import token as token_domain
from app.domain.auth import user as user_domain

from .dependencies import authentication as authentication_dependencies
from .dependencies import registration as registration_dependencies
from .dependencies import user as user_dependencies

router = APIRouter()


@router.post("/login/access-token", response_model=token_domain.Token, name="user:access-token")
async def login_access_token(
    result: Annotated[token_domain.Token, Depends(authentication_dependencies.login_access_token)]
) -> token_domain.Token:
    return result


@router.get("/login/me", response_model=user_domain.User, name="user:me")
async def read_users_me(
    result: Annotated[user_domain.User, Depends(user_dependencies.read_users_me)]
) -> user_domain.User:
    return result


@router.post("/register", response_model=user_domain.User, name="user:create-user")
async def create_user(
    result: Annotated[user_domain.User, Depends(registration_dependencies.create_user)]
) -> user_domain.User:
    """
    Endpoint for registering a new user
    """
    return result
