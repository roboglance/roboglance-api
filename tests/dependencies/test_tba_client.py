from contextlib import asynccontextmanager

from fastapi import HTTPException
from httpx import AsyncClient
from pytest import raises

from app.dependencies.settings import RoboGlanceSettings
from app.dependencies.tba_client import get_tba_client


async def test_get_tba_client_should_return_correct_class_instance():
    settings = RoboGlanceSettings.model_construct(tba_api_key="fake_tba_api_key")
    get_tba_client_with_context = asynccontextmanager(get_tba_client)

    async with get_tba_client_with_context(settings) as tba_client:
        assert isinstance(tba_client, AsyncClient)

        assert tba_client.base_url.is_absolute_url

        assert tba_client.headers.get("X-TBA-Auth-Key") == "fake_tba_api_key"


async def test_get_tba_client_should_raise_error_when_no_api_key_in_env_var():
    settings = RoboGlanceSettings.model_construct()
    get_tba_client_with_context = asynccontextmanager(get_tba_client)
    with raises(HTTPException, match="The Blue Alliance") as exception_info:
        async with get_tba_client_with_context(settings) as _tba_client:
            pass
    assert exception_info.value.status_code == 500
