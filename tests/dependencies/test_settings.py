from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from app.dependencies.settings import RoboGlanceSettings, get_settings


def test_settings_should_load_env_vars(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ROBOGLANCE_TBA_API_KEY", "fake_tba_api_key")
    assert RoboGlanceSettings(_env_file=None).tba_api_key == "fake_tba_api_key"


def test_settings_should_not_load_missing_env_vars(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.delenv("ROBOGLANCE_TBA_API_KEY", raising=False)
    assert RoboGlanceSettings(_env_file=None).tba_api_key is None


def test_get_settings_should_return_correct_class_instance(
    mocker: MockerFixture,
):
    get_settings.cache_clear()
    mock_settings_class = mocker.patch(
        "app.dependencies.settings.RoboGlanceSettings", autospec=True
    )
    mock_settings_instance = mock_settings_class.return_value

    assert get_settings() is mock_settings_instance


def test_get_settings_called_multiple_times_should_only_call_constructor_once(
    mocker: MockerFixture,
):
    get_settings.cache_clear()
    mock_settings_class = mocker.patch(
        "app.dependencies.settings.RoboGlanceSettings", autospec=True
    )

    get_settings()
    get_settings()
    mock_settings_class.assert_called_once()
