import pytest

from app.core.security import verify_password, get_password_hash


def test_verify_password():
    hashed = get_password_hash("amazing")
    assert verify_password("amazing", hashed)