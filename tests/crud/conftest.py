from typing import Callable

import pytest

from app.schemas.user import UserCreate


@pytest.fixture
def user_schema() -> Callable[..., UserCreate]:
    """
    This fixture returns a User schema object.

    """

    def _make_user_schema(*, password: str, email: str, full_name: str) -> UserCreate:
        return UserCreate(password=password, email=email, full_name=full_name)

    return _make_user_schema
