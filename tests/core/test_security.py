from contextlib import nullcontext as does_not_raise
from datetime import timedelta
from time import sleep
from typing import Any, ContextManager, Optional
from unittest import mock

import pytest
from jose import ExpiredSignatureError, JWTError

from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_verify_password() -> None:
    hashed = get_password_hash("amazing")
    assert verify_password("amazing", hashed)


@pytest.mark.parametrize(
    ("subject", "additional_string", "expires_delta", "expired", "expectation"),
    [
        # I really hope this test does not fail...hopefully faster than 999 days
        ("vlad", "", timedelta(days=999), False, does_not_raise()),
        ("vlad", "", None, False, does_not_raise()),
        # TODO: obviously this needs to change...next post
        ("vlad", "", timedelta(microseconds=1), True, pytest.raises(ExpiredSignatureError)),
        ("vlad", "_i_4m_a_h4ck3r", None, False, pytest.raises(JWTError)),
    ],
)
@mock.patch("app.core.security.settings")
def test_encoding_decoding_tokens(
    # the following comes from our patch
    settings_mock: mock.MagicMock,
    # the following comes from our test pytest parameters
    subject: str,
    additional_string: str,
    expires_delta: Optional[timedelta],
    expired: bool,
    expectation: ContextManager[Any],
) -> None:
    settings_mock.ACCESS_TOKEN_EXPIRE_MINUTES = 10
    settings_mock.SECRET_KEY = "wowsosecret"

    encoded_token: str = create_access_token(subject=subject, expires_delta=expires_delta)
    if expired and expires_delta:
        sleep(expires_delta.microseconds)
    with expectation:
        payload = decode_access_token(encoded_token + additional_string)
        assert payload["sub"] == subject
