from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient

from app.dependencies.tba_client import TbaClientDependency


class TbaService:
    _tba_client: AsyncClient

    def __init__(self, tba_client: TbaClientDependency):
        self._tba_client = tba_client

    async def is_tba_healthy(self) -> bool:
        response = await self._tba_client.get("/status")
        return response.is_success


TbaServiceDependency = Annotated[TbaService, Depends(TbaService)]
