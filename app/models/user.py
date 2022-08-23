from typing import Optional

from sqlalchemy import Boolean, Column, String

from app.db.base import Base


class User(Base):

    __tablename__ = "users"

    full_name: Optional[str] = Column(String, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True, nullable=False)
    is_superuser: bool = Column(Boolean(), default=False, nullable=False)
