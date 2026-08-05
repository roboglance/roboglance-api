from collections.abc import Callable
from typing import Any

from fastapi.testclient import TestClient
from pytest import fixture
from pytest_mock import MockFixture, MockType

from app.dependencies.tba_service import TbaService
from app.dependencies.team_service import TeamService
from app.main import app


@fixture
def dependency_overrides():
    yield app.dependency_overrides
    app.dependency_overrides = {}


DependencyOverrides = dict[Callable[..., Any], Callable[..., MockType]]


@fixture
def mock_tba_service(
    mocker: MockFixture,
    dependency_overrides: DependencyOverrides,
) -> MockType:
    mock = mocker.create_autospec(TbaService, spec_set=True)
    dependency_overrides[TbaService] = lambda: mock
    return mock


@fixture
def mock_team_service(
    mocker: MockFixture,
    dependency_overrides: DependencyOverrides,
) -> MockType:
    mock = mocker.create_autospec(TeamService, spec_set=True)
    dependency_overrides[TeamService] = lambda: mock
    return mock


@fixture
def test_client():
    with TestClient(app) as client:
        yield client
