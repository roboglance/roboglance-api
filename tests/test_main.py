from contextlib import asynccontextmanager

from fastapi import HTTPException
from pytest import raises
from pytest_mock import MockerFixture

from app.main import get_settings, get_tba_service
from app.settings import RoboGlanceSettings
from app.tba_service import TbaService


def test_get_settings_should_return_correct_class_instance(
    mocker: MockerFixture,
):
    get_settings.cache_clear()
    mock_settings_class = mocker.patch("app.main.RoboGlanceSettings", autospec=True)
    mock_settings_instance = mock_settings_class.return_value

    assert get_settings() is mock_settings_instance


def test_get_settings_called_multiple_times_should_only_call_constructor_once(
    mocker: MockerFixture,
):
    get_settings.cache_clear()
    mock_settings_class = mocker.patch("app.main.RoboGlanceSettings", autospec=True)

    get_settings()
    get_settings()
    mock_settings_class.assert_called_once()


async def test_get_tba_service_should_return_correct_class_instance():
    settings = RoboGlanceSettings.model_construct(tba_api_key="fake_tba_api_key")
    get_tba_context = asynccontextmanager(get_tba_service)

    async with get_tba_context(settings) as tba_service:
        assert isinstance(tba_service, TbaService)

        tba_client_base_url = tba_service.tba_client.base_url
        assert tba_client_base_url.is_absolute_url

        tba_client_api_key = tba_service.tba_client.headers.get("X-TBA-Auth-Key")
        assert tba_client_api_key == "fake_tba_api_key"


async def test_get_tba_service_should_raise_error_when_no_api_key_in_env_var():
    settings = RoboGlanceSettings.model_construct()
    get_tba_context = asynccontextmanager(get_tba_service)
    with raises(HTTPException, match="The Blue Alliance") as exception_info:
        async with get_tba_context(settings):
            pass
    assert exception_info.value.status_code == 500
