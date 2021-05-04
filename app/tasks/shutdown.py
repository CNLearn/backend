from typing import Callable
from fastapi import FastAPI

from app.db.connections import close_postgres_database_connection


def database_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_db() -> None:
        await close_postgres_database_connection(app)
    return stop_db
