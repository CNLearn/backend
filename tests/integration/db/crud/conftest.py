from typing import Callable

import pytest

from app.domain.auth import user as user_domain


@pytest.fixture
def user_schema() -> Callable[..., user_domain.UserCreate]:
    """
    This fixture returns a User schema object.

    """

    def _make_user_schema(*, password: str, email: str, full_name: str) -> user_domain.UserCreate:
        return user_domain.UserCreate(password=password, email=email, full_name=full_name)

    return _make_user_schema
