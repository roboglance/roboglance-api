from fastapi.testclient import TestClient
from pytest_mock import MockType

from app.dependencies.team_service import NonExistentTeamError, Team


def test_get_frc_team_should_return_team_when_given_existent_team_number(
    test_client: TestClient,
    mock_team_service: MockType,
):
    mock_team_service.get_team.return_value = Team(
        team_name="The Strange Quarks",
    )
    response = test_client.get("/teams/frc/6101")
    assert response.status_code == 200
    assert response.json() == {"team_name": "The Strange Quarks"}


def test_get_frc_team_should_raise_client_error_when_given_non_existent_team_number(
    test_client: TestClient,
    mock_team_service: MockType,
):
    mock_team_service.get_team.side_effect = NonExistentTeamError("Team not found.")
    response = test_client.get("/teams/frc/6101")
    mock_team_service.get_team.assert_called_once()
    assert response.status_code == 404


def test_get_frc_team_should_raise_client_error_when_given_invalid_team_number(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/-6101")
    mock_team_service.get_team.assert_not_called()
    assert response.is_client_error


def test_get_frc_team_should_raise_client_error_when_given_string(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/sixty-one-oh-one")
    mock_team_service.get_team.assert_not_called()
    assert response.is_client_error


def test_get_frc_team_should_raise_client_error_when_given_valid_team_number_with_letter(
    test_client: TestClient,
    mock_team_service: MockType,
):
    response = test_client.get("/teams/frc/6101a")
    mock_team_service.get_team.assert_not_called()
    assert response.is_client_error
