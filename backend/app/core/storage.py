# backend/app/core/storage.py
"""Simple storage utilities for saving uploaded images to disk.

This is intentionally minimal and synchronous: suitable for small prototypes.
"""
from pathlib import Path
import uuid


def save_image_bytes(target_dir: Path, content: bytes, filename: str | None = None) -> Path:
    """Save raw image bytes to a file inside `target_dir` and return Path object.

    - If filename is provided, we'll sanitize by appending a random uuid to avoid collisions.
    - Returns the path of the saved file.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_name = (filename or "image")
    # Append a uuid to the filename
    name_parts = safe_name.rsplit('.', maxsplit=1)
    if len(name_parts) == 2:
        base, ext = name_parts
        out_name = f"{base}_{uuid.uuid4().hex[:8]}.{ext}"
    else:
        out_name = f"{safe_name}_{uuid.uuid4().hex[:8]}"

    out_path = target_dir / out_name
    with open(out_path, 'wb') as f:
        f.write(content)

    return out_path
