# backend/app/api/endpoints/inference.py
"""
API endpoints for Hugging Face model inference.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel

from app.core.config import Settings, get_settings
from app.core.services.huggingface import query_huggingface_api
from app.core import index as index_core
from app.core import storage as core_storage
from pathlib import Path
import os

router = APIRouter()

class EmbeddingRequest(BaseModel):
    text: str

@router.post("/caption")
async def get_image_caption(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    """
    Receives an image file and returns a caption from the Hugging Face API.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    image_bytes = await file.read()
    try:
        response = await query_huggingface_api(
            model_url=settings.HUGGING_FACE_IMAGE_CAPTION_MODEL,
            api_key=settings.HUGGING_FACE_API_KEY,
            data=image_bytes,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embedding")
async def get_text_embedding(
    request: EmbeddingRequest, settings: Settings = Depends(get_settings)
):
    """
    Receives text and returns embeddings from the Hugging Face API.
    """
    payload = {"inputs": request.text}
    try:
        response = await query_huggingface_api(
            model_url=settings.HUGGING_FACE_EMBEDDING_MODEL,
            api_key=settings.HUGGING_FACE_API_KEY,
            json_payload=payload,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SearchRequest(BaseModel):
    text: str | None = None
    k: int | None = 5


@router.post("/images/upload")
async def upload_image(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    image_bytes = await file.read()
    # Save the file into project data directory
    base_dir = Path(os.getenv("DATA_DIR", Path.cwd()))
    images_dir = base_dir / "data" / "images"
    saved = core_storage.save_image_bytes(images_dir, image_bytes, file.filename)

    # Get caption using HF model
    try:
        caption_resp = await query_huggingface_api(
            model_url=settings.HUGGING_FACE_IMAGE_CAPTION_MODEL,
            api_key=settings.HUGGING_FACE_API_KEY,
            data=image_bytes,
        )
        # Some models return a list or dict depending on payload; normalize
        if isinstance(caption_resp, list):
            caption_text = caption_resp[0].get("generated_text") if caption_resp else ""
        elif isinstance(caption_resp, dict):
            caption_text = caption_resp.get("generated_text") or caption_resp.get("caption") or ""
        else:
            caption_text = str(caption_resp)
    except Exception:
        caption_text = ""

    # Get embedding
    try:
        emb_response = await query_huggingface_api(
            model_url=settings.HUGGING_FACE_EMBEDDING_MODEL,
            api_key=settings.HUGGING_FACE_API_KEY,
            json_payload={"inputs": caption_text or ""},
        )
        # Normalize embedding
        if isinstance(emb_response, dict) and emb_response.get("embedding"):
            embedding = emb_response["embedding"]
        elif isinstance(emb_response, list):
            # Some embedding APIs return a list of float arrays
            embedding = emb_response[0]
        else:
            embedding = []
    except Exception:
        embedding = []

    # Insert into in-memory index
    from uuid import uuid4

    item_id = str(uuid4())
    index_core.add_item(item_id, saved.name, caption_text, embedding)
    return {"id": item_id, "filename": saved.name, "caption": caption_text}


@router.post("/search")
async def search(req: SearchRequest, settings: Settings = Depends(get_settings)):
    # text-based search -> compute embedding and find top k
    text = req.text
    k = req.k or 5
    if not text:
        return {"results": []}
    try:
        emb_response = await query_huggingface_api(
            model_url=settings.HUGGING_FACE_EMBEDDING_MODEL,
            api_key=settings.HUGGING_FACE_API_KEY,
            json_payload={"inputs": text},
        )
        if isinstance(emb_response, dict) and emb_response.get("embedding"):
            query_embedding = emb_response["embedding"]
        elif isinstance(emb_response, list):
            query_embedding = emb_response[0]
        else:
            query_embedding = []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    results = index_core.search_by_embedding(query_embedding, k=k)
    return {"results": results}


@router.get('/images/list')
async def list_images():
    items = index_core.list_items()
    return {"images": items}


@router.get('/images/{filename}')
async def get_image(filename: str):
    base_dir = Path(os.getenv("DATA_DIR", Path.cwd()))
    images_dir = base_dir / "data" / "images"
    file_path = images_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    from fastapi.responses import FileResponse
    return FileResponse(path=str(file_path), media_type="image/jpeg")
