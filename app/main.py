from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from httpx import AsyncClient
from pydantic import BaseModel

from .tba_service import TbaService
from .settings import RoboGlanceSettings

app = FastAPI()


@lru_cache
def get_settings():
    return RoboGlanceSettings()


async def get_tba_service(
    settings: Annotated[RoboGlanceSettings, Depends(get_settings)],
):
    if settings.tba_api_key is None:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error. Missing API key for accessing The Blue Alliance.",
        )

    async with AsyncClient(
        base_url="https://www.thebluealliance.com/api/v3",
        headers={"X-TBA-Auth-Key": settings.tba_api_key},
    ) as tba_client:
        yield TbaService(tba_client)


class RoboGlanceStatus(BaseModel):
    healthy: bool
    the_blue_alliance_healthy: bool


@app.get("/status")
async def read_status(
    tba_service: Annotated[TbaService, Depends(get_tba_service)],
) -> RoboGlanceStatus:

    tba_healthy = await tba_service.is_tba_healthy()

    results = RoboGlanceStatus(
        healthy=tba_healthy,
        the_blue_alliance_healthy=tba_healthy,
    )
    return results
