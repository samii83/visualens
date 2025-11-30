# backend/utils.py
# Purpose: Helper utilities used by the backend for image processing, I/O, and indexing.
# TODO: Implement:
# - image decoding/validation utilities
# - helper to save and load images from a local data folder
# - small wrapper or adapter for a simple vector index (in-memory or FAISS)
# - generate thumbnails for UI
# - basic cache and cleanup utilities

# Keep functions pure and not tied to FastAPI-specific types so they can be tested easily.
