from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import database, user
from app.core.security import create_access_token
from app.crud.crud_user import user as crud_user
from app.schemas.token import Token
from app.schemas.user import User
from app.settings.base import settings

router = APIRouter()


@router.post("/login/access-token", response_model=Token, name="user:access-token")
async def login_access_token(
    db: AsyncSession = Depends(database.get_async_session), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud_user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.get("/login/me", response_model=User, name="user:me")
async def read_users_me(current_user: User = Depends(user.get_current_user)) -> Any:
    return current_user
