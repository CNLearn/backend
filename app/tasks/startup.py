from typing import Awaitable, Callable

from fastapi import FastAPI

from app.db.connections import open_postgres_database_connection


def database_start_app_handler(app: FastAPI) -> Callable[[], Awaitable[None]]:
    async def start_db() -> None:
        await open_postgres_database_connection(app)

    return start_db
