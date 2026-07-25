from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from app.tba_service import TbaService

app = FastAPI()


class RoboGlanceStatus(BaseModel):
    healthy: bool
    the_blue_alliance_healthy: bool


@app.get("/status")
async def read_status(
    tba_service: Annotated[TbaService, Depends(TbaService)],
) -> RoboGlanceStatus:
    tba_healthy = await tba_service.is_tba_healthy()

    results = RoboGlanceStatus(
        healthy=tba_healthy,
        the_blue_alliance_healthy=tba_healthy,
    )
    return results
