from httpx import AsyncClient


class TbaService:
    def __init__(self, tba_client: AsyncClient):
        self.tba_client = tba_client

    async def is_tba_healthy(self) -> bool:
        response = await self.tba_client.get("/status")
        return response.is_success
