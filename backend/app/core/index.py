# backend/app/core/index.py
"""Simple in-memory vector index for prototype use only.

Provides add_item and search functions using cosine similarity.
"""
from math import sqrt
from typing import List, Dict, Any

_INDEX: List[Dict[str, Any]] = []


def _dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(a: List[float]) -> float:
    return sqrt(sum(x * x for x in a))


def add_item(item_id: str, filename: str, caption: str, embedding: List[float]) -> None:
    """Add an item to the index."""
    _INDEX.append({
        "id": item_id,
        "filename": filename,
        "caption": caption,
        "embedding": embedding,
    })


def list_items():
    return _INDEX


def search_by_embedding(query_embedding: List[float], k: int = 5):
    """Return top-k results ordered by cosine similarity (desc).

    This does naive loop and sorting — acceptable for small prototypes.
    """
    if not _INDEX:
        return []

    results = []

    q_norm = _norm(query_embedding)
    if q_norm == 0:
        return []

    for it in _INDEX:
        emb = it.get("embedding")
        if not emb:
            continue
        dot = _dot(query_embedding, emb)
        emb_norm = _norm(emb)
        if emb_norm == 0:
            continue
        score = dot / (q_norm * emb_norm)
        results.append({"id": it["id"], "filename": it["filename"], "caption": it["caption"], "score": score})

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:k]
