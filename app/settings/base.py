import secrets
from typing import List

from pydantic import AnyHttpUrl

from .core import CNLearnBaseSettings, CNLearnSettings


class Settings(CNLearnBaseSettings):
    # Application settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    APP_NAME: str
    VERSION: str

    # password settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


app_settings = CNLearnSettings[Settings](Settings)()
