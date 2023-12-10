from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions, security
from app.db.crud.user import user_crud
from app.domain.auth import token as token_domain
from app.settings.base import app_settings


async def login_access_token(db: AsyncSession, form_data: OAuth2PasswordRequestForm) -> token_domain.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    possible_user = await user_crud.authenticate(db, email=form_data.username, password=form_data.password)
    if not possible_user:
        raise exceptions.CNLearnWithMessage(status_code=400, message="Incorrect email or password")
    elif not user_crud.is_active(possible_user):
        raise exceptions.CNLearnWithMessage(status_code=400, message="Inactive user")
    access_token_expires = timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return token_domain.Token(
        access_token=security.create_access_token(possible_user.id, expires_delta=access_token_expires),
        token_type="bearer",
    )
