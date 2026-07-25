from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException
from httpx import AsyncClient

from app.settings import RoboGlanceSettings


@lru_cache
def get_settings():
    return RoboGlanceSettings()


async def get_tba_client(
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
        yield tba_client
