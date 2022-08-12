import os
from typing import Callable, Optional

import alembic
from alembic.config import Config
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient, Response
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud import user
from app.models.user import User


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture(scope="session")
def app(apply_migrations: None) -> FastAPI:
    from app.server import create_application

    return create_application()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://testserver", headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest_asyncio.fixture
async def get_async_session(client: AsyncClient, app: FastAPI) -> AsyncSession:
    async_session_maker = app.state._db
    async with async_session_maker() as async_session:
        yield async_session


@pytest_asyncio.fixture
async def clean_users_table(get_async_session: AsyncSession):
    yield
    db: AsyncSession = get_async_session
    await db.execute(delete(User))
    await db.commit()


@pytest_asyncio.fixture
async def create_user_object(get_async_session: AsyncSession):
    async def _create_user(email: str, password: str, full_name: Optional[str] = None) -> User:
        db: AsyncSession = get_async_session
        user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
        new_user = await user.create(db, obj_in=user_in)
        return new_user

    return _create_user


@pytest_asyncio.fixture
async def return_logged_in_user_bearer_token(
    get_async_session: AsyncSession,
    create_user_object: Callable[..., User],
    client: AsyncClient,
    app: FastAPI,
):
    async def _get_logged_in_user_token(email: str, password: str):
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
        json_response: dict[str, str] = response.json()
        token: str = json_response["access_token"]
        return token

    return _get_logged_in_user_token
