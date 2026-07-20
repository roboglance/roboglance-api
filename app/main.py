from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from .tba_client import TbaClient
from .settings import RoboGlanceSettings

app = FastAPI()


@lru_cache
def get_settings():
    return RoboGlanceSettings()


class RoboGlanceStatus(BaseModel):
    healthy: bool
    the_blue_alliance_healthy: bool


@app.get("/status")
async def read_status(
    settings: Annotated[RoboGlanceSettings, Depends(get_settings)],
) -> RoboGlanceStatus:
    tba_healthy = await TbaClient.is_tba_healthy(settings.tba_api_key)

    results = RoboGlanceStatus(
        healthy=tba_healthy,
        the_blue_alliance_healthy=tba_healthy,
    )
    return results
