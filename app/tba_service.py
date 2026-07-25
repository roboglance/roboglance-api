from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient

from app.main import get_tba_client


class TbaService:
    _tba_client: AsyncClient

    def __init__(self, tba_client: Annotated[AsyncClient, Depends(get_tba_client)]):
        self._tba_client = tba_client

    async def is_tba_healthy(self) -> bool:
        response = await self._tba_client.get("/status")
        return response.is_success
