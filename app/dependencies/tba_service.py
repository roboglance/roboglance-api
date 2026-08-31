from http import HTTPStatus
from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient
from pydantic import BaseModel

from app.dependencies.tba_client import TbaClientDependency


class TbaTeam(BaseModel):
    team_number: int
    nickname: str
    name: str
    school_name: str | None
    city: str | None
    state_prov: str | None
    country: str | None


class NonExistentTbaTeamError(Exception):
    pass


class TbaService:
    _tba_client: AsyncClient

    def __init__(self, tba_client: TbaClientDependency):
        self._tba_client = tba_client

    async def is_tba_healthy(self) -> bool:
        response = await self._tba_client.get("/status")
        return response.is_success

    async def get_team(self, team_number: int) -> TbaTeam:
        response = await self._tba_client.get(f"/team/frc{team_number}")
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NonExistentTbaTeamError
        response.raise_for_status()
        return TbaTeam.model_validate(response.json())


type TbaServiceDependency = Annotated[TbaService, Depends(TbaService)]
