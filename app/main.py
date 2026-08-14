from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from app.dependencies.tba_service import TbaServiceDependency

app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
)


@app.get("/openapi.yaml", include_in_schema=False)
async def openapi_yaml() -> PlainTextResponse:
    import yaml  # noqa: PLC0415 -- only import bulky yaml library when needed

    return PlainTextResponse(
        content=yaml.dump(app.openapi(), sort_keys=False),
        media_type="application/yaml",
    )


class RoboGlanceStatus(BaseModel):
    healthy: bool
    the_blue_alliance_healthy: bool


@app.get("/status")
async def read_status(
    tba_service: TbaServiceDependency,
) -> RoboGlanceStatus:
    tba_healthy = await tba_service.is_tba_healthy()

    return RoboGlanceStatus(
        healthy=tba_healthy,
        the_blue_alliance_healthy=tba_healthy,
    )
