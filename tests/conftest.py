import os
from typing import AsyncGenerator, Awaitable, Callable, Generator, Optional

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient, Response
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import alembic.command
from alembic.config import Config
from app.db.crud.user import user_crud
from app.db.models import user as user_model
from app.domain.auth import user as user_domain
from app.settings.db import db_settings
from tests.fixtures.vocabulary import add_some_words_and_characters
from tests.fixtures.vocabulary import (
    generate_character_model as generate_character_model,
)
from tests.fixtures.vocabulary import (
    generate_character_schema as generate_character_schema,
)
from tests.fixtures.vocabulary import generate_word_model as generate_word_model
from tests.fixtures.vocabulary import generate_word_schema as generate_word_schema

# from sqlalchemy import event


# if the wrong environment, stop tests
@pytest.fixture(scope="session", autouse=True)
def check_environment() -> Generator[None, None, None]:
    if os.getenv("ENVIRONMENT") != "Testing":
        raise Exception("Tests can only be run in a testing environment")
    yield


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session", autouse=True)
def apply_migrations(check_environment: Callable[[None], None]) -> Generator[None, None, None]:
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    add_some_words_and_characters()
    print("added sample data")
    yield
    alembic.command.downgrade(config, "base")


@pytest.mark.asyncio
@pytest.fixture
async def get_async_session_no_transaction() -> AsyncGenerator[AsyncSession, None]:
    ASYNC_URI: str = str(db_settings.CNLEARN_POSTGRES_URI)
    engine = create_async_engine(ASYNC_URI, echo=False)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session_maker() as async_session:
        yield async_session


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def get_async_db_session_transaction() -> AsyncGenerator[AsyncSession, None]:
    # please read https://github.com/sqlalchemy/sqlalchemy/issues/5812 for more informations
    # on async db sessions with transactional capabilities.
    # the actual transaction is done at the (Async)Connection level rather than session level
    async_engine: AsyncEngine = create_async_engine(
        str(db_settings.CNLEARN_POSTGRES_URI),
        echo=False,  # , json_serializer=orjson.dumps, json_deserializer=orjson.loads
    )
    async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    )

    connection = await async_engine.connect()
    trans = await connection.begin()
    async_session = async_session_maker(bind=connection)

    # nested = await connection.begin_nested()

    # @event.listens_for(async_session.sync_session, "after_transaction_end")
    # def end_savepoint(session, transaction) -> None:
    #    nonlocal nested
    #    if not nested.is_active:
    #        nested = connection.sync_connection.begin_nested()
    yield async_session

    await trans.rollback()
    await async_session.close()
    await connection.close()


# Create a new application for testing
@pytest.fixture(scope="session")
def app() -> FastAPI:
    from app.app import create_application

    local_app = create_application()
    return local_app
    # return create_application()


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
async def clean_users_table(get_async_session_no_transaction: AsyncSession) -> AsyncGenerator[None, None]:
    yield
    db: AsyncSession = get_async_session_no_transaction
    await db.execute(delete(user_model.User))
    await db.commit()


@pytest.mark.asyncio
@pytest.fixture
async def create_user_object(
    get_async_session_no_transaction: AsyncSession,
) -> Callable[..., Awaitable[user_model.User]]:
    async def _create_user(email: str, password: str, full_name: Optional[str] = None) -> user_model.User:
        db: AsyncSession = get_async_session_no_transaction
        user_in = user_domain.UserCreate(password=password, email=email, full_name=full_name)
        new_user = await user_crud.create(db, obj_in=user_in)
        return new_user

    return _create_user


@pytest.mark.asyncio
@pytest.fixture
async def return_logged_in_user_bearer_token(
    get_async_session_no_transaction: AsyncSession,
    create_user_object: Callable[..., Awaitable[user_model.User]],
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
