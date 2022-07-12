import os

import alembic
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy import delete

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
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
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
    users_deleted: CursorResult = await db.execute(delete(User))
    await db.commit()
