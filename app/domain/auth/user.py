from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None


# Additional properties to return via API
class User(UserInDBBase):
    pass
