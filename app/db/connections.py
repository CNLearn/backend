
from sqlalchemy.orm.session import sessionmaker
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, close_all_sessions
import logging

from app.settings.base import settings

logger = logging.getLogger(__name__)


async def open_postgres_database_connection(app: FastAPI) -> None:
    # these are configured in the settings module
    ASYNC_URI: str = settings.SQLALCHEMY_POSTGRES_URI.replace(
        "postgresql", "postgresql+asyncpg", 1)
    engine = create_async_engine(ASYNC_URI, echo=True)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    try:
        async with async_session() as session:
            await session.execute("SELECT 1")
        app.state._db = async_session
        logging.info("You have connected to the database")
    except Exception as e:
        logger.warn("ERROR OCCURRED WHILE CONNECTING TO THE DATABASE")
        logger.warn(e)
        logger.warn("ERROR OCCURRED WHILE CONNECTING TO THE DATABASE")


async def close_postgres_database_connection(app: FastAPI) -> None:
    try:
        close_all_sessions()
        logging.info("DB connection closed")
    except Exception as e:
        logger.warn("ERROR OCCURRED WHILE CLOSING ALL THE SESSIONS")
        logger.warn(e)
        logger.warn("ERROR OCCURRED WHILE CLOSING ALL THE SESSIONS")
