import os
from typing import AsyncGenerator, Awaitable, Callable, Generator, Optional

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient, Response
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import alembic.command
from alembic.config import Config
from app.crud.crud_user import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.settings.base import settings
from tests.fixtures.vocabulary import add_some_words_and_characters


# if the wrong environment, stop tests
@pytest.fixture(scope="session", autouse=True)
def check_environment() -> Generator[None, None, None]:
    if os.getenv("ENVIRONMENT") != "Testing":
        raise Exception("Tests can only be run in a testing environment")
    yield


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations(check_environment: Callable[[None], None]) -> Generator[None, None, None]:
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope="session")
def insert_sample_data(apply_migrations: Generator[None, None, None]) -> Generator[None, None, None]:
    add_some_words_and_characters()
    yield


# Create a new application for testing
@pytest.fixture(scope="session")
def app(insert_sample_data: Generator[None, None, None]) -> FastAPI:
    from app.app import create_application

    return create_application()


@pytest.mark.asyncio
@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            app=manager.app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.mark.asyncio
@pytest.fixture
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    ASYNC_URI: str = str(settings.SQLALCHEMY_POSTGRES_URI)
    engine = create_async_engine(ASYNC_URI, echo=False)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session_maker() as async_session:
        yield async_session


@pytest.mark.asyncio
@pytest.fixture
async def clean_users_table(get_async_session: AsyncSession) -> AsyncGenerator[None, None]:
    yield
    db: AsyncSession = get_async_session
    await db.execute(delete(User))
    await db.commit()


@pytest.mark.asyncio
@pytest.fixture
async def create_user_object(get_async_session: AsyncSession) -> Callable[..., Awaitable[User]]:
    async def _create_user(email: str, password: str, full_name: Optional[str] = None) -> User:
        db: AsyncSession = get_async_session
        user_in = UserCreate(password=password, email=email, full_name=full_name)
        new_user = await crud_user.create(db, obj_in=user_in)
        return new_user

    return _create_user


@pytest.mark.asyncio
@pytest.fixture
async def return_logged_in_user_bearer_token(
    get_async_session: AsyncSession,
    create_user_object: Callable[..., Awaitable[User]],
    client: AsyncClient,
    app: FastAPI,
) -> Callable[..., Awaitable[str]]:
    async def _get_logged_in_user_token(email: str, password: str) -> str:
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
