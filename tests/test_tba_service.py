from httpx import AsyncClient, Response
from pytest_mock import MockerFixture

from app.tba_service import TbaService


async def test_is_tba_healthy_should_be_true_if_response_is_success(
    mocker: MockerFixture,
):
    mock_tba_client = mocker.create_autospec(AsyncClient, spec_set=True)
    mock_response = mocker.create_autospec(Response, spec_set=True)
    mock_tba_client.get.return_value = mock_response
    mock_response.is_success = True

    tba_service = TbaService(mock_tba_client)
    assert await tba_service.is_tba_healthy() is True
    mock_tba_client.get.assert_called_once_with("/status")


async def test_is_tba_healthy_should_be_false_if_response_is_not_success(
    mocker: MockerFixture,
):
    mock_tba_client = mocker.create_autospec(AsyncClient, spec_set=True)
    mock_response = mocker.create_autospec(Response, spec_set=True)
    mock_tba_client.get.return_value = mock_response
    mock_response.is_success = False

    tba_service = TbaService(mock_tba_client)
    assert await tba_service.is_tba_healthy() is False
    mock_tba_client.get.assert_called_once_with("/status")
