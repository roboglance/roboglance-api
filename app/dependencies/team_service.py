from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel


class Team(BaseModel):
    team_name: str


class NonExistentTeamError(Exception):
    pass


class TeamService:
    async def get_team(self, team_number: int) -> Team:
        raise NotImplementedError("get_team not implemented")


TeamServiceDependency = Annotated[TeamService, Depends(TeamService)]
