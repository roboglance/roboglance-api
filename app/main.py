from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class HealthResponse(BaseModel):
    healthy: bool


@app.get("/health-check")
def read_health() -> HealthResponse:
    return HealthResponse(healthy=True)
