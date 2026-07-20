from pydantic_settings import BaseSettings, SettingsConfigDict


class RoboGlanceSettings(BaseSettings):
    tba_api_key: str | None = None

    model_config = SettingsConfigDict(env_prefix="RoboGlance_")
