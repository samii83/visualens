# Backend (FastAPI) - VisuaLens

This folder contains the FastAPI backend for VisuaLens.

Quick Notes:
- Run in dev: `uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000`
- Check `.env.example` for environment variables.
- Implemented endpoints should follow the spec described in the root README.

TODO:
- Implement /caption, /embeddings, /search, /images endpoints.
- Add tests, CI, and example curl commands.
