from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import PositiveInt

from app.dependencies.team_service import (
    Team,
    TeamServiceDependency,
)
from app.errors import NonexistentTeamError

router = APIRouter(prefix="/teams")


@router.get("/frc/{team_number}")
async def get_team(
    team_number: PositiveInt,
    team_service: TeamServiceDependency,
) -> Team:
    try:
        return await team_service.get_team(team_number)
    except NonexistentTeamError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
