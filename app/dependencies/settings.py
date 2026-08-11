from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class RoboGlanceSettings(BaseSettings):
    tba_api_key: str | None = None

    model_config = SettingsConfigDict(env_prefix="RoboGlance_", env_file=".env")


@lru_cache
def get_settings() -> RoboGlanceSettings:
    return RoboGlanceSettings()


type SettingsDependency = Annotated[RoboGlanceSettings, Depends(get_settings)]
