from httpx import AsyncClient, HTTPStatusError, MockTransport
from pytest import raises
from respx import Router

from app.dependencies.tba_service import TbaService, TbaTeam
from app.errors import NonexistentTeamError


async def test_is_tba_healthy_should_be_true_if_response_is_success():
    router = Router(base_url="https://example.com/api")
    router.get("/status").respond(200)

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        assert await tba_service.is_tba_healthy() is True
        router.assert_all_called()


async def test_is_tba_healthy_should_be_false_if_response_is_not_success():
    router = Router(base_url="https://example.com/api")
    router.get("/status").respond(500)

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        assert await tba_service.is_tba_healthy() is False
        router.assert_all_called()


async def test_get_team_returns_existing_team_with_full_info():
    router = Router(base_url="https://example.com/api")
    router.get("/team/frc6101").respond(
        200,
        json={
            "team_number": 6101,
            "nickname": "The Strange Quarks",
            "name": "Washtenaw Technical Middle College",
            "school_name": "Washtenaw Technical Middle College",
            "city": "Ann Arbor",
            "state_prov": "MI",
            "country": "United States of America",
        },
    )

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        assert await tba_service.get_team(6101) == TbaTeam(
            team_number=6101,
            nickname="The Strange Quarks",
            name="Washtenaw Technical Middle College",
            school_name="Washtenaw Technical Middle College",
            city="Ann Arbor",
            state_prov="MI",
            country="United States of America",
        )
        router.assert_all_called()


async def test_get_team_returns_nonexistent_team():
    router = Router(base_url="https://example.com/api")
    router.get("/team/frc6101").respond(
        404, json={"Error": "frc6101 is not a valid team key"}
    )

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        with raises(NonexistentTeamError):
            await tba_service.get_team(6101)
        router.assert_all_called()


async def test_get_team_missing_auth_info():
    router = Router(base_url="https://example.com/api")
    router.get("/team/frc6101").respond(
        401,
        json={
            "Error": "X-TBA-Auth-Key is a required header or URL param. Please get an access key at http://www.thebluealliance.com/account."
        },
    )

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        with raises(HTTPStatusError):
            await tba_service.get_team(6101)
        router.assert_all_called()


async def test_get_team_returns_existing_team_with_null_fields():
    router = Router(base_url="https://example.com/api")
    router.get("/team/frc6101").respond(
        200,
        json={
            "team_number": 6101,
            "nickname": "The Strange Quarks",
            "name": "Washtenaw Technical Middle College",
            "school_name": None,
            "city": None,
            "state_prov": None,
            "country": None,
        },
    )

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        assert await tba_service.get_team(6101) == TbaTeam(
            team_number=6101,
            nickname="The Strange Quarks",
            name="Washtenaw Technical Middle College",
            school_name=None,
            city=None,
            state_prov=None,
            country=None,
        )
        router.assert_all_called()


async def test_get_team_returns_existing_team_with_some_null_fields():
    router = Router(base_url="https://example.com/api")
    router.get("/team/frc6101").respond(
        200,
        json={
            "team_number": 6101,
            "nickname": "The Strange Quarks",
            "name": "Washtenaw Technical Middle College",
            "school_name": None,
            "city": "Ann Arbor",
            "state_prov": "MI",
            "country": None,
        },
    )

    async with AsyncClient(
        base_url="https://example.com/api",
        transport=MockTransport(router.async_handler),
    ) as mock_tba_client:
        tba_service = TbaService(mock_tba_client)
        assert await tba_service.get_team(6101) == TbaTeam(
            team_number=6101,
            nickname="The Strange Quarks",
            name="Washtenaw Technical Middle College",
            school_name=None,
            city="Ann Arbor",
            state_prov="MI",
            country=None,
        )
        router.assert_all_called()
