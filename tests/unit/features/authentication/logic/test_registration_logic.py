from unittest import mock

import pytest

from app.core import exceptions
from app.db.crud.user import user_crud
from app.domain.auth import user as user_domain
from app.features.auth.logic.registration import create_user


@pytest.mark.asyncio
@mock.patch.object(user_crud, "get_by_email")
async def test_create_user_user_exists(
    # the following is a mock patch
    mock_get_by_email: mock.AsyncMock,
) -> None:
    mock_get_by_email.return_value = mock.Mock()
    with pytest.raises(exceptions.CNLearnWithMessage):
        await create_user(db=mock.MagicMock(), password="", email="", full_name="")


@pytest.mark.asyncio
@mock.patch.object(user_crud, "create")
@mock.patch.object(user_crud, "get_by_email")
async def test_create_user_validation_fails(
    # the following is a mock patch
    mock_get_by_email: mock.AsyncMock,
    mock_create: mock.AsyncMock,
) -> None:
    mock_get_by_email.return_value = None
    mock_create.return_value = mock.Mock(full_name="", email="")
    with pytest.raises(exceptions.CNLearnWithMessage):
        await create_user(db=mock.MagicMock(), password="heytheregoodpassword", email="hi@there.com", full_name="Hi Hi")


@pytest.mark.asyncio
@mock.patch.object(user_domain.User, "model_validate")
@mock.patch.object(user_crud, "create")
@mock.patch.object(user_crud, "get_by_email")
async def test_create_user_everything_works(
    # the following is a mock patch
    mock_get_by_email: mock.AsyncMock,
    mock_create: mock.AsyncMock,
    mock_model_validate: mock.MagicMock,
) -> None:
    mock_get_by_email.return_value = None
    mock_create.return_value = mock.Mock()
    sample_user_schema = user_domain.User(
        email="hi@there.com", is_active=True, is_superuser=False, full_name="Hi Hi", id=1
    )
    mock_model_validate.return_value = sample_user_schema
    result = await create_user(
        db=mock.MagicMock(), password="heytheregoodpassword", email="hi@there.com", full_name="Hi Hi"
    )
    assert result == sample_user_schema
