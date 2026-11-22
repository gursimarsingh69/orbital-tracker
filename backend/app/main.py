from fastapi import FastAPI
from app.api.v1.endpoints import satellites

app = FastAPI(
    title="OrbitWatch API",
    description="Intelligent Space Situational Awareness Platform",
    version="0.2.0"
)


@app.get("/")
def root():
    return {
        "project": "OrbitWatch",
        "status": "running"
    }


@app.get("/api/v1/health")
def health():
    return {
        "status": "healthy",
        "service": "OrbitWatch Backend"
    }


app.include_router(
    satellites.router,
    prefix="/api/v1/satellites",
    tags=["Satellite Tracking"]
)
