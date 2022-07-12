from typing import Callable, Any

from fastapi import FastAPI
from httpx import AsyncClient, Response
import pytest


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, app: FastAPI, clean_users_table: Callable[..., None]):
    create_user_url: str = app.url_path_for("user:create-user")
    response: Response = await client.post(
        url=create_user_url,
        json={
            "password": "interesting",
            "email": "unique@email.com",
            "full_name": "Uniquely Interesting",
        }
    )
    json_response: dict[str, Any] = response.json()
    assert json_response["email"] == "unique@email.com"
    assert json_response["is_active"] is True
    assert json_response["is_superuser"] is False
    assert json_response["full_name"] == "Uniquely Interesting"
    assert isinstance(json_response["id"], int)
