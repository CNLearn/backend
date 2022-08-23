import secrets
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):

    # Application settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    APP_NAME: str
    VERSION: str

    # PostgreSQL database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    TESTING: int  # if this is 1, we will connect to the testing database
    SQLALCHEMY_POSTGRES_URI: Optional[PostgresDsn] = None
    # if the last one is None, let's build it ourselves

    @validator("SQLALCHEMY_POSTGRES_URI", pre=True)
    def create_postgres_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        postgres_db_name: str = values.get("POSTGRES_DB", "")
        if values.get("TESTING", 0):
            postgres_db_name += "_testing"

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{postgres_db_name}",
            port=f"{values.get('POSTGRES_PORT')}",
        )

    # password settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    class Config:
        case_sensitive = True


class DevSettings(Settings):
    class Config:
        env_file = ".dev.env"
        env_file_encoding = "utf-8"


class TestSettings(Settings):
    class Config:
        env_file = ".test.env"
        env_file_encoding = "utf-8"


class StageSettings(Settings):
    class Config:
        env_file = ".stage.env"
        env_file_encoding = "utf-8"


class ProdSettings(Settings):
    class Config:
        env_file = ".prod.env"
        env_file_encoding = "utf-8"


settings = DevSettings()
