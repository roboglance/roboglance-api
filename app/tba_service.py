from httpx import AsyncClient


class TbaService:
    async def is_tba_healthy(api_key: str | None) -> bool:
        if api_key is None:
            return False

        async with AsyncClient(
            base_url="https://www.thebluealliance.com/api/v3",
            headers={"X-TBA-Auth-Key": api_key},
        ) as tba_client:
            response = await tba_client.get("/status")
            return response.is_success
