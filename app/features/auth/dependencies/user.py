from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth import user as user_domain
from app.features.db import get_async_session
from app.settings.base import app_settings

from ..logic import user as user_logic

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{app_settings.API_V1_STR}/login/access-token")


async def read_users_me(
    db: AsyncSession = Depends(get_async_session), token: str = Depends(reusable_oauth2)
) -> user_domain.User:
    return await user_logic.get_current_user(db, token)
