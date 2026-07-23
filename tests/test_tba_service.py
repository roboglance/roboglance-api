from httpx import AsyncClient, MockTransport
from respx import Router

from app.tba_service import TbaService


async def test_is_tba_healthy_should_be_true_if_response_is_success():
    router = Router(base_url="https://example.com/api")
    router.get("/status").respond(200)

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        assert await tba_service.is_tba_healthy() is True
        router.assert_all_called()


async def test_is_tba_healthy_should_be_false_if_response_is_not_success():
    router = Router(base_url="https://example.com/api")
    router.get("/status").respond(500)

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        assert await tba_service.is_tba_healthy() is False
        router.assert_all_called()
