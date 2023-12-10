from fastapi import Body, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth import user as user_domain
from app.features.db import get_async_session

from ..logic import registration as registration_logic


async def create_user(
    *,
    db: AsyncSession = Depends(get_async_session),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> user_domain.User:
    return await registration_logic.create_user(db=db, password=password, email=email, full_name=full_name)
