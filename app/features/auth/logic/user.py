from fastapi import status
from jose import ExpiredSignatureError, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions, security
from app.db.crud import user
from app.domain.auth import token as token_domain
from app.domain.auth import user as user_domain


async def get_current_user(db: AsyncSession, token: str) -> user_domain.User:
    try:
        payload = security.decode_access_token(token)
    except (JWTError, ExpiredSignatureError):
        raise exceptions.CNLearnWithMessage(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Could not validate credentials",
        )
    try:
        token_data = token_domain.TokenPayload(sub=int(payload.sub))
    except (ValidationError, ValueError):
        raise exceptions.CNLearnWithMessage(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Could not validate credentials",
        )
    possible_user = await user.user_crud.get(db, id=token_data.sub)
    if not possible_user:
        raise exceptions.CNLearnWithMessage(status_code=404, message="User not found")
    try:
        user_schema = user_domain.User.model_validate(possible_user)
    except ValidationError:
        raise exceptions.CNLearnWithMessage(status_code=500, message="Problem with current user")
    return user_schema
