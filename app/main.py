from fastapi import FastAPI
from pydantic import BaseModel

from app.dependencies.tba_service import TbaServiceDependency
from app.dependencies.team_service import Team, TeamServiceDependency

app = FastAPI()


class RoboGlanceStatus(BaseModel):
    healthy: bool
    the_blue_alliance_healthy: bool


@app.get("/status")
async def read_status(
    tba_service: TbaServiceDependency,
) -> RoboGlanceStatus:
    tba_healthy = await tba_service.is_tba_healthy()

    return RoboGlanceStatus(
        healthy=tba_healthy,
        the_blue_alliance_healthy=tba_healthy,
    )


# TODO @zalhabash: Add ability to find team by name?
@app.get("/teams/{team_number}")
async def team_from_number(
    team_number: int,
    team_service: TeamServiceDependency,
) -> Team:
    return await team_service.find_team(team_number)
