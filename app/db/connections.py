import logging

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import close_all_sessions, sessionmaker

from app.settings.base import settings

logger = logging.getLogger(__name__)


async def open_postgres_database_connection(app: FastAPI) -> None:
    # these are configured in the settings module

    if settings.SQLALCHEMY_POSTGRES_URI is None:
        return
    ASYNC_URI: str = settings.SQLALCHEMY_POSTGRES_URI.replace("postgresql", "postgresql+asyncpg", 1)
    engine = create_async_engine(ASYNC_URI, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    try:
        app.state._db = async_session
        logging.info("You have connected to the database")
    except Exception as e:
        logger.warning("ERROR OCCURRED WHILE CONNECTING TO THE DATABASE")
        logger.warning(e)
        logger.warning("ERROR OCCURRED WHILE CONNECTING TO THE DATABASE")


async def close_postgres_database_connection(app: FastAPI) -> None:
    try:
        close_all_sessions()
        logging.info("DB connection closed")
    except Exception as e:
        logger.warn("ERROR OCCURRED WHILE CLOSING ALL THE SESSIONS")
        logger.warn(e)
        logger.warn("ERROR OCCURRED WHILE CLOSING ALL THE SESSIONS")
