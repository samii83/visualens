# backend/app/main.py
"""
Main FastAPI application entrypoint.
Sets up CORS, routers, and basic middleware.
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import inference
from app.core.config import get_settings

app = FastAPI(title="VisuaLens Backend")

# Get settings instance
settings = get_settings()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inference.router, prefix="/api/v1")

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the VisuaLens API"}


@app.get('/images/{filename}')
def get_image_root(filename: str):
    base_dir = Path(os.getenv("DATA_DIR", Path.cwd()))
    images_dir = base_dir / "data" / "images"
    file_path = images_dir / filename
    if not file_path.exists():
        return FileResponse(str(Path(__file__).with_name('README.md')))
    return FileResponse(str(file_path))
