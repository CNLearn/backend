from pydantic import EmailStr, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions
from app.db.crud.user import user_crud
from app.domain.auth import user as user_domain


async def create_user(
    *,
    db: AsyncSession,
    password: str,
    email: EmailStr,
    full_name: str,
) -> user_domain.User:
    # first, check if such a user does not already exist
    existing_user = await user_crud.get_by_email(db, email=email)
    if existing_user:
        raise exceptions.CNLearnWithMessage(status_code=400, message="This email is already in use.")
    user_in = user_domain.UserCreate(password=password, email=email, full_name=full_name)
    new_user = await user_crud.create(db, obj_in=user_in)
    try:
        user_schema = user_domain.User.model_validate(new_user)
    except ValidationError:
        raise exceptions.CNLearnWithMessage(status_code=500, message="There is an error with this user object.")

    return user_schema
