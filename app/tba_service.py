from httpx import AsyncClient


class TbaService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def is_tba_healthy(self) -> bool:
        async with AsyncClient(
            base_url="https://www.thebluealliance.com/api/v3",
            headers={"X-TBA-Auth-Key": self.api_key},
        ) as tba_client:
            response = await tba_client.get("/status")
            return response.is_success
