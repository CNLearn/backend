from typing import Any, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.domain.auth import user as user_domain

from ..models import user as user_models
from .base import CRUDBase


class CRUDUser(CRUDBase[user_models.User, user_domain.UserCreate, user_domain.UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[user_models.User]:
        result = await db.execute(select(user_models.User).where(user_models.User.email == email))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: user_domain.UserCreate) -> user_models.User:
        db_obj = user_models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: user_models.User, obj_in: Union[user_domain.UserUpdate, dict[str, Any]]
    ) -> user_models.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[user_models.User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: user_models.User) -> bool:
        return user.is_active

    def is_superuser(self, user: user_models.User) -> bool:
        return user.is_superuser


user_crud = CRUDUser(user_models.User)
