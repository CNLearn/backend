import os
import secrets
from typing import Any, List, Literal

from pydantic import AnyHttpUrl, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["Development", "Staging", "Production", "Testing"]


class Settings(BaseSettings):
    # Application settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ENVIRONMENT: Environment

    APP_NAME: str
    VERSION: str

    # PostgreSQL database settings
    POSTGRES_SCHEMA: str = "postgresql+asyncpg"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    SQLALCHEMY_POSTGRES_URI: PostgresDsn

    # password settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    @model_validator(mode="before")
    def something_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        scheme: str = "postgresql+asyncpg"
        postgres_db_name: str = str(data["POSTGRES_DB"])
        user: str = str(data["POSTGRES_USER"])
        password: str = str(data["POSTGRES_PASSWORD"])
        host: str = str(data["POSTGRES_SERVER"])
        port: int = int(data["POSTGRES_PORT"])
        url = f"{scheme}://{user}:{password}@{host}:{port}/{postgres_db_name}"
        data["SQLALCHEMY_POSTGRES_URI"] = PostgresDsn(url)
        return data


class DevSettings(Settings):
    model_config = SettingsConfigDict(env_file=".dev.env", env_file_encoding="utf-8")


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=".testing.env", env_file_encoding="utf-8")


class StagingSettings(Settings):
    # TODO: think about having these in some secrets/depending on deployment
    model_config = SettingsConfigDict(env_file=".staging.env", env_file_encoding="utf-8")


class ProdSettings(Settings):
    # TODO: think about having these in some secrets/depending on deployment
    model_config = SettingsConfigDict(env_file=".production.env", env_file_encoding="utf-8")


def get_settings() -> DevSettings | TestSettings | StagingSettings | ProdSettings:
    environment: str = os.getenv("ENVIRONMENT", "")
    settings: DevSettings | TestSettings | StagingSettings | ProdSettings
    match environment:
        case "Production":
            settings = ProdSettings.model_validate({"ENVIRONMENT": "Production"})
        case "Staging":
            settings = StagingSettings.model_validate({"ENVIRONMENT": "Staging"})
        case "Development":
            settings = DevSettings.model_validate({"ENVIRONMENT": "Development"})
        case "Testing":
            settings = TestSettings.model_validate({"ENVIRONMENT": "Testing"})
        case _:
            raise ValueError("Unknown environment passed")
    return settings


settings = get_settings()
