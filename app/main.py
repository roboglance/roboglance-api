from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from httpx import AsyncClient

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
    tba_healthy = await is_tba_healthy(settings.tba_api_key)

    results = RoboGlanceStatus(
        healthy=tba_healthy,
        the_blue_alliance_healthy=tba_healthy,
    )
    return results


async def is_tba_healthy(api_key: str | None) -> bool:
    if api_key is None:
        return False

    async with AsyncClient() as client:
        response = await client.get(
            "https://www.thebluealliance.com/api/v3/status",
            headers={"X-TBA-Auth-Key": api_key},
        )
        return response.is_success
