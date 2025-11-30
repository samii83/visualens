# backend/models.py
# Purpose: Pydantic models for request/response validation and documentation.
# TODO: Define the following Pydantic models:
# - CaptionRequest: { image: bytes | reference }
# - CaptionResponse: { caption: str, alternatives: list[str], confidence?: float }
# - EmbeddingRequest: { image: bytes | text }
# - EmbeddingResponse: { embedding: list[float] }
# - SearchRequest: { query_text?: str, query_image?: bytes, k?: int }
# - SearchResult: { id: str, caption: str, score: float, thumbnail_path?: str }
# - Generic API wrapper / Error models

# The file should only contain schema definitions and any common types used by endpoints.
