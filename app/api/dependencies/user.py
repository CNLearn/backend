from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api.dependencies import database
from app.core import security
from app.models.user import User
from app.settings.base import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


async def get_current_user(
    db: AsyncSession = Depends(database.get_async_session), token: str = Depends(reusable_oauth2)
) -> User:
    print(token)
    try:
        payload = security.decode_access_token(token)
        print(payload)
        token_data = schemas.TokenPayload(**payload)
        print(token_data)
    except (JWTError, ExpiredSignatureError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
