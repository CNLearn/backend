import logging
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.api.dependencies import database
from app.crud import user

router: APIRouter = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/register", response_model=schemas.User, name="user:create-user")
async def create_user(
    *,
    db: AsyncSession = Depends(database.get_async_session),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Endpoint for registering a new user
    """
    # first, check if such a user does not already exist
    existing_user = await user.get_by_email(db, email=email)
    if existing_user:
        raise HTTPException(status_code=400, detail="This email is already in use.")
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    new_user = await user.create(db, obj_in=user_in)
    return new_user
