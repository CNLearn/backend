from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth import token as token_domain
from app.features.db import get_async_session

from ..logic import authentication as authentication_logic


async def login_access_token(
    db: AsyncSession = Depends(get_async_session), form_data: OAuth2PasswordRequestForm = Depends()
) -> token_domain.Token:
    return await authentication_logic.login_access_token(db, form_data)
