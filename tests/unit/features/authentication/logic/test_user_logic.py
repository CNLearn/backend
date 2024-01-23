from unittest import mock

import pytest
from jose import JWTError

from app.core import exceptions, security
from app.db.crud.user import user_crud
from app.domain.auth import user as user_domain
from app.features.auth.logic.user import get_current_user


@pytest.mark.asyncio
@mock.patch.object(security, "decode_access_token")
async def test_get_current_user_jwt_error(
    # the following is a mock patch
    mock_decode_access_token: mock.MagicMock,
) -> None:
    mock_decode_access_token.side_effect = [JWTError]
    with pytest.raises(exceptions.CNLearnWithMessage):
        await get_current_user(mock.MagicMock(), "")


@pytest.mark.asyncio
@mock.patch.object(security, "decode_access_token")
async def test_get_current_user_invalid_token_payload(
    # the following is a mock patch
    mock_decode_access_token: mock.MagicMock,
) -> None:
    mock_decode_access_token.return_value = mock.Mock(sub="")
    with pytest.raises(exceptions.CNLearnWithMessage):
        await get_current_user(mock.MagicMock(), "")


@pytest.mark.asyncio
@mock.patch.object(user_crud, "get")
@mock.patch.object(security, "decode_access_token")
async def test_get_current_user_no_user(
    # the following is a mock patch
    mock_decode_access_token: mock.MagicMock,
    mock_user_crud_get: mock.AsyncMock,
) -> None:
    mock_decode_access_token.return_value = mock.Mock(sub="1")
    mock_user_crud_get.return_value = None
    with pytest.raises(exceptions.CNLearnWithMessage):
        await get_current_user(mock.MagicMock(), "")


@pytest.mark.asyncio
@mock.patch.object(user_crud, "get")
@mock.patch.object(security, "decode_access_token")
async def test_get_current_user_user_validation_error(
    # the following is a mock patch
    mock_decode_access_token: mock.MagicMock,
    mock_user_crud_get: mock.AsyncMock,
) -> None:
    mock_decode_access_token.return_value = mock.Mock(sub="1")
    mock_user_crud_get.return_value = mock.Mock(not_enough="info")
    with pytest.raises(exceptions.CNLearnWithMessage):
        await get_current_user(mock.MagicMock(), "")


@pytest.mark.asyncio
@mock.patch.object(user_crud, "get")
@mock.patch.object(security, "decode_access_token")
async def test_get_current_user_everything_works(
    # the following is a mock patch
    mock_decode_access_token: mock.MagicMock,
    mock_user_crud_get: mock.AsyncMock,
) -> None:
    mock_decode_access_token.return_value = mock.Mock(sub="1")
    mock_user_crud_get.return_value = mock.Mock(
        full_name="hi there", email="my@email.com", id=1, is_active=True, is_superuser=False
    )
    result = await get_current_user(mock.MagicMock(), "")
    assert isinstance(result, user_domain.User)
