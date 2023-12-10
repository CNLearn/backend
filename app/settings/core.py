import os
from typing import Generic, Literal, TypeVar

from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["Development", "Production", "Testing"]

SettingsClass = TypeVar("SettingsClass", bound=BaseSettings)


class CNLearnBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8", extra="ignore")
    ENVIRONMENT: Environment


class CNLearnSettings(Generic[SettingsClass]):
    def __init__(self, settings_class: type[SettingsClass]) -> None:
        self.settings_class: type[SettingsClass] = settings_class

    def __call__(self) -> SettingsClass:
        environment: str = os.getenv("ENVIRONMENT", "")
        match environment:
            case "Development":
                settings = self.settings_class(_env_file=".dev.env", ENVIRONMENT="Development")
            case "Production":
                settings = self.settings_class(_env_file=".production.env", ENVIRONMENT="Production")
            case "Testing":
                settings = self.settings_class(_env_file=".testing.env", ENVIRONMENT="Testing")
            case _:
                raise ValueError("Unknown environment passed")
        return settings
