from collections.abc import Callable
from typing import Any

from fastapi.testclient import TestClient
from pytest import fixture
from pytest_mock import MockFixture, MockType

from app.dependencies.tba_service import TbaService
from app.dependencies.team_service import NonExistentTeamError, Team, TeamService
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


def test_frc_team_from_number_should_return_team_when_given_existent_team_number(
    test_client: TestClient,
    mock_team_service: MockType,
):
    mock_team_service.find_team.return_value = Team(
        team_name="The Strange Quarks",
    )
    response = test_client.get("/teams/frc/6101")
    assert response.status_code == 200
    assert response.json() == {"team_name": "The Strange Quarks"}


def test_frc_team_from_number_should_raise_client_error_when_given_non_existent_team_number(
    test_client: TestClient,
    mock_team_service: MockType,
):
    mock_team_service.find_team.side_effect = NonExistentTeamError("Team not found.")
    response = test_client.get("/teams/frc/6101")
    mock_team_service.find_team.assert_called_once()
    assert response.status_code == 404


def test_frc_team_from_number_should_raise_client_error_when_given_invalid_team_number(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/-6101")
    mock_team_service.find_team.assert_not_called()
    assert response.is_client_error


def test_frc_team_from_number_should_raise_client_error_when_given_string(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/sixty-one-oh-one")
    mock_team_service.find_team.assert_not_called()
    assert response.is_client_error


def test_frc_team_from_number_should_raise_client_error_when_given_valid_team_number_beginning_with_char(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/a6101")
    mock_team_service.find_team.assert_not_called()
    assert response.is_client_error


def test_frc_team_from_number_should_raise_client_error_when_given_valid_team_number_ending_with_char(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/6101a")
    mock_team_service.find_team.assert_not_called()
    assert response.is_client_error


def test_frc_team_from_number_should_raise_client_error_when_given_valid_team_number_containing_char(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/6a101")
    mock_team_service.find_team.assert_not_called()
    assert response.is_client_error
