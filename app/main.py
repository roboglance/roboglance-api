from fastapi import FastAPI
from pydantic import BaseModel

from app.dependencies.tba_service import TbaServiceDependency
from app.routers import teams

app = FastAPI()


class RoboGlanceStatus(BaseModel):
    healthy: bool
    the_blue_alliance_healthy: bool


@app.get("/status")
async def get_status(
    tba_service: TbaServiceDependency,
) -> RoboGlanceStatus:
    tba_healthy = await tba_service.is_tba_healthy()

    return RoboGlanceStatus(
        healthy=tba_healthy,
        the_blue_alliance_healthy=tba_healthy,
    )


app.include_router(teams.router)
