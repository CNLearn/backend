import contextlib
from typing import AsyncGenerator, TypedDict

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import close_all_sessions

from app.settings.base import settings


class AppState(TypedDict):
    _db: async_sessionmaker[AsyncSession]


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[AppState, None]:
    if settings.SQLALCHEMY_POSTGRES_URI is None:
        return
    ASYNC_URI: str = settings.SQLALCHEMY_POSTGRES_URI
    engine = create_async_engine(ASYNC_URI, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield AppState(_db=async_session)
    close_all_sessions()
