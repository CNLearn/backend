import contextlib
from typing import AsyncGenerator, TypedDict

import jieba
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import close_all_sessions

from app.settings.db import db_settings


class AppState(TypedDict):
    _db: async_sessionmaker[AsyncSession]
    _chinese_segmenter: jieba


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[AppState, None]:
    ASYNC_URI: str = str(db_settings.CNLEARN_POSTGRES_URI)
    engine = create_async_engine(ASYNC_URI, echo=False)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    jieba.initialize()
    yield AppState(_db=async_session_maker, _chinese_segmenter=jieba)
    close_all_sessions()
