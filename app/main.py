from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveInt

from app.dependencies.tba_service import TbaServiceDependency
from app.dependencies.team_service import (
    NonExistentTeamError,
    Team,
    TeamServiceDependency,
)

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


@app.get("/teams/frc/{team_number}")
async def get_team(
    team_number: PositiveInt,
    team_service: TeamServiceDependency,
) -> Team:
    try:
        return await team_service.get_team(team_number)
    except NonExistentTeamError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
