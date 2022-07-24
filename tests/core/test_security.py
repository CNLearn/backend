from app.core.security import get_password_hash, verify_password


def test_verify_password():
    hashed = get_password_hash("amazing")
    assert verify_password("amazing", hashed)
