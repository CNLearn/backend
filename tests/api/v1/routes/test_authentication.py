from typing import Any, Awaitable, Callable

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response

from app.models.user import User


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, app: FastAPI, clean_users_table: Callable[[None], None]) -> None:
    create_user_url: str = app.url_path_for("user:create-user")
    response: Response = await client.post(
        url=create_user_url,
        json={
            "password": "interesting",
            "email": "unique@email.com",
            "full_name": "Uniquely Interesting",
        },
    )
    json_response: dict[str, Any] = response.json()
    assert json_response["email"] == "unique@email.com"
    assert json_response["is_active"] is True
    assert json_response["is_superuser"] is False
    assert json_response["full_name"] == "Uniquely Interesting"
    assert isinstance(json_response["id"], int)


@pytest.mark.asyncio
async def test_login_access_token(
    client: AsyncClient,
    app: FastAPI,
    create_user_object: Callable[..., Awaitable[User]],
    clean_users_table: Callable[[None], None],
) -> None:
    email: str = "admin@cnlearn.app"
    password: str = "thisissecret"
    await create_user_object(email=email, password=password)

    # now let's hit the login endpoint
    login_url: str = app.url_path_for("user:access-token")
    response: Response = await client.post(
        url=login_url,
        data={
            "username": email,
            "password": password,
        },
        # we need to change the client's headers content-type
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    json_response: dict[str, Any] = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_access_token_fail(
    client: AsyncClient,
    app: FastAPI,
) -> None:
    # let's hit the login endpoint
    login_url: str = app.url_path_for("user:access-token")
    response: Response = await client.post(
        url=login_url,
        data={
            "username": "email@notexist.com",
            "password": "badbadpassword",
        },
        # we need to change the client's headers content-type
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    json_response: dict[str, Any] = response.json()
    assert json_response == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_read_users_me(
    client: AsyncClient,
    app: FastAPI,
    return_logged_in_user_bearer_token: Callable[..., Awaitable[str]],
    clean_users_table: Callable[[None], None],
) -> None:
    email: str = "free@cnlearn.app"
    password: str = "paid"
    token: str = await return_logged_in_user_bearer_token(email=email, password=password)
    headers = {"Authorization": f"Bearer {token}"}
    me_url: str = app.url_path_for("user:me")
    response: Response = await client.get(
        url=me_url,
        headers=headers,
    )
    json_response: dict[str, Any] = response.json()
    assert response.status_code == 200
    assert json_response["email"] == email
    assert json_response["is_active"]
    assert not json_response["is_superuser"]
    assert json_response["full_name"] is None
    assert isinstance(json_response["id"], int)


@pytest.mark.asyncio
async def test_read_users_me_fail(
    client: AsyncClient,
    app: FastAPI,
) -> None:
    me_url: str = app.url_path_for("user:me")
    response: Response = await client.get(
        url=me_url,
    )
    assert response.status_code == 401
    json_response: dict[str, Any] = response.json()
    assert json_response == {"detail": "Not authenticated"}
