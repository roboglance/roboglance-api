from pytest import MonkeyPatch

from app.settings import RoboGlanceSettings


def test_settings_should_load_env_vars(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ROBOGLANCE_TBA_API_KEY", "fake_tba_api_key")
    assert RoboGlanceSettings().tba_api_key == "fake_tba_api_key"


def test_settings_should_not_load_missing_env_vars(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.delenv("ROBOGLANCE_TBA_API_KEY", raising=False)
    assert RoboGlanceSettings().tba_api_key is None
