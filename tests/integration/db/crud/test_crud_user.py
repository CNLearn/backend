from typing import Callable, Optional, Sequence
from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.user import user_crud
from app.db.models import user as user_model
from app.domain.auth import user as user_domain


@mock.patch(f"{user_crud.__module__}.verify_password")
@mock.patch(f"{user_crud.__module__}.get_password_hash")
@pytest.mark.asyncio
async def test_user_crud(
    mocked_get_password_hash: mock.MagicMock,
    mocked_verify_password: mock.MagicMock,
    get_async_session: AsyncSession,
    user_schema: Callable[..., user_domain.UserCreate],
    # the following are root conftest fixtures
    client: AsyncClient,
    clean_users_table: Callable[[None], None],
) -> None:
    # let's first call user get with nothing in there
    no_user: Optional[user_model.User] = await user_crud.get(get_async_session, id=1)
    assert no_user is None

    mocked_get_password_hash.return_value = "MockedPassword"
    user_in: user_domain.UserCreate = user_schema(password="amazing", email="user@email.com", full_name="Fake Name")
    new_user: user_model.User = await user_crud.create(get_async_session, obj_in=user_in)
    assert new_user.email == "user@email.com"
    assert new_user.full_name == "Fake Name"
    assert new_user.hashed_password == "MockedPassword"
    assert new_user.is_active
    assert not new_user.is_superuser

    # let's get the new_user.id since that can vary depending on what other tests ran first
    user_id: int = new_user.id

    # now let's call user get again and we should have one with the same id
    existing_user: Optional[user_model.User] = await user_crud.get(get_async_session, id=user_id)
    assert isinstance(existing_user, user_model.User)

    # let's call get_multi and see that there are in fact 1 user(s)
    users: Sequence[user_model.User] = await user_crud.get_multi(get_async_session)
    assert len(users) == 1

    # you want to change your email? ok let's do that
    user_schema_in = user_domain.UserUpdate(email="newuser@email.com")
    updated_user: user_model.User = await user_crud.update(get_async_session, db_obj=new_user, obj_in=user_schema_in)
    assert updated_user.email == "newuser@email.com"

    # you even want to change your password? ok let's generate a new mock return_value
    mocked_get_password_hash.return_value = "MockedPassword2"
    user_schema_in = user_domain.UserUpdate(password="getsoverwrittenbythehash")
    updated_user = await user_crud.update(get_async_session, db_obj=updated_user, obj_in=user_schema_in)
    assert updated_user.hashed_password == "MockedPassword2"

    # do you think we can find you by email? let's see
    user_by_email: Optional[user_model.User] = await user_crud.get_by_email(
        get_async_session, email="newuser@email.com"
    )
    assert isinstance(user_by_email, user_model.User)
    assert user_by_email.email == "newuser@email.com"
    assert user_by_email.id == user_id

    user_no_such_email: Optional[user_model.User] = await user_crud.get_by_email(
        get_async_session, email="fake@email.com"
    )
    assert user_no_such_email is None

    # let's check whether the user is active and is a superuser. by default, it will be True and False respectively
    assert user_crud.is_active(updated_user) is True
    assert user_crud.is_superuser(updated_user) is False

    # let's log our user in. we will enter an email that does not exist first
    no_logged_in_user: Optional[user_model.User] = await user_crud.authenticate(
        get_async_session,
        email="fake@email.com",
        password="asd",
    )
    assert no_logged_in_user is None

    # ok now we forgot our password momentarily
    mocked_verify_password.return_value = False
    incorrect_password_no_user: Optional[user_model.User] = await user_crud.authenticate(
        get_async_session,
        email="newuser@email.com",
        password="asd",
    )
    assert incorrect_password_no_user is None
    assert mocked_verify_password.called

    # ooooh I remember the password now
    mocked_verify_password.return_value = True
    correct_password_user: Optional[user_model.User] = await user_crud.authenticate(
        get_async_session,
        email="newuser@email.com",
        password="doesntmatter",
    )
    assert isinstance(correct_password_user, user_model.User)
    assert mocked_verify_password.called

    # you want to leave us? :( well, I am sorry to hear that
    removed_user: Optional[user_model.User] = await user_crud.remove(get_async_session, id=user_id)
    assert isinstance(removed_user, user_model.User)
    # let's check that there's no one left
    assert len(await user_crud.get_multi(get_async_session)) == 0
