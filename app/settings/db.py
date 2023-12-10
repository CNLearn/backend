"""
This module contains the database settings for CNLearn.
"""
from pydantic import PostgresDsn, computed_field

from .core import CNLearnBaseSettings, CNLearnSettings


class DataBaseSettings(CNLearnBaseSettings):
    POSTGRES_SCHEMA: str = "postgresql+asyncpg"
    CNLEARN_POSTGRES_DB: str
    CNLEARN_POSTGRES_USER: str
    CNLEARN_POSTGRES_PASSWORD: str
    CNLEARN_POSTGRES_SERVER: str
    CNLEARN_POSTGRES_PORT: int

    @computed_field  # type: ignore[misc]
    @property
    def CNLEARN_POSTGRES_URI(self) -> PostgresDsn:
        scheme = "postgresql+asyncpg"
        user: str = self.CNLEARN_POSTGRES_USER
        password: str = self.CNLEARN_POSTGRES_PASSWORD
        host: str = self.CNLEARN_POSTGRES_SERVER
        path: str = f"/{self.CNLEARN_POSTGRES_DB}"
        port: int = self.CNLEARN_POSTGRES_PORT
        url = f"{scheme}://{user}:{password}@{host}:{port}{path}"
        return PostgresDsn(url)


db_settings = CNLearnSettings[DataBaseSettings](DataBaseSettings)()
