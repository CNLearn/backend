from unittest import mock

import pytest

from app.core import exceptions
from app.db.crud.user import user_crud
from app.domain.auth import token as token_domain
from app.features.auth.logic.authentication import login_access_token


@pytest.mark.asyncio
@mock.patch.object(user_crud, "authenticate")
async def test_login_access_token_no_user(
    # the following is a mock patch
    mock_authenticate: mock.AsyncMock,
) -> None:
    mock_authenticate.return_value = None
    with pytest.raises(exceptions.CNLearnWithMessage):
        await login_access_token(mock.MagicMock(), mock.MagicMock())


@pytest.mark.asyncio
@mock.patch.object(user_crud, "authenticate")
async def test_login_access_token_user_not_active(
    # the following is a mock patch
    mock_authenticate: mock.AsyncMock,
) -> None:
    mock_authenticate.return_value = mock.Mock(is_active=False)
    with pytest.raises(exceptions.CNLearnWithMessage):
        await login_access_token(mock.MagicMock(), mock.MagicMock())


@pytest.mark.asyncio
@mock.patch.object(user_crud, "authenticate")
async def test_login_access_token_returns_token(
    # the following is a mock patch
    mock_authenticate: mock.AsyncMock,
) -> None:
    mock_authenticate.return_value = mock.Mock(is_active=True)
    result = await login_access_token(mock.MagicMock(), mock.MagicMock())
    assert isinstance(result, token_domain.Token)
