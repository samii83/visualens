# backend/app/api/endpoints/inference.py
"""
API endpoints for Hugging Face model inference.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel

from app.core.config import Settings, get_settings
from app.core.services.huggingface import query_huggingface_api

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
