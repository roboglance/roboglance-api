from fastapi.testclient import TestClient
from pytest_mock import MockType


async def test_status_should_be_healthy_when_tba_is_healthy(
    test_client: TestClient,
    mock_tba_service: MockType,
):
    mock_tba_service.is_tba_healthy.return_value = True
    response = test_client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"healthy": True, "the_blue_alliance_healthy": True}


async def test_status_should_not_be_healthy_when_tba_is_not_healthy(
    test_client: TestClient,
    mock_tba_service: MockType,
):
    mock_tba_service.is_tba_healthy.return_value = False
    response = test_client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"healthy": False, "the_blue_alliance_healthy": False}
