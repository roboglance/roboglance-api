from collections.abc import Callable
from typing import Any

from fastapi.testclient import TestClient
from pytest import fixture
from pytest_mock import MockFixture, MockType

from app.dependencies.tba_service import TbaService
from app.main import app


@fixture
def dependency_overrides():
    yield app.dependency_overrides
    app.dependency_overrides = {}


DependencyOverrides = dict[Callable[..., Any], Callable[..., MockType]]


@fixture
def mock_tba_service(mocker: MockFixture, dependency_overrides: DependencyOverrides):
    mock = mocker.create_autospec(TbaService, spec_set=True)
    dependency_overrides[TbaService] = lambda: mock
    return mock


@fixture
def test_client():
    with TestClient(app) as client:
        yield client


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
