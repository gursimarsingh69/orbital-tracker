from fastapi import FastAPI

app = FastAPI(
    title="OrbitWatch API",
    description="Intelligent Space Situational Awareness Platform",
    version="0.1.0"
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
