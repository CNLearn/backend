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
    SQLALCHEMY_POSTGRES_URI: Optional[PostgresDsn] = None
    # if the last one is None, let's build it ourselves

    @validator('SQLALCHEMY_POSTGRES_URI', pre=True)
    def create_postgres_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRESS_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=f"{values.get('POSTGRES_PORT')}",
        )

    class Config:
        case_sensitive = True


class DevSettings(Settings):
    class Config:
        env_file = '.dev.env'
        env_file_encoding = 'utf-8'


class StageSettings(Settings):
    class Config:
        env_file = '.stage.env'
        env_file_encoding = 'utf-8'


class ProdSettings(Settings):
    class Config:
        env_file = '.prod.env'
        env_file_encoding = 'utf-8'


settings = DevSettings()
