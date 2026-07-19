import os
from fastapi import FastAPI
from pydantic import BaseModel
from httpx import AsyncClient

app = FastAPI()


class RoboGlanceStatus(BaseModel):
    healthy: bool
    the_blue_alliance_healthy: bool


tba_api_key = os.getenv("THE_BLUE_ALLIANCE_API_KEY")


@app.get("/status")
async def read_status() -> RoboGlanceStatus:
    tba_healthy = await is_tba_healthy(tba_api_key)

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
