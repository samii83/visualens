# backend/app/services/huggingface.py
"""
Service for interacting with the Hugging Face Inference API.
"""
import httpx
import random

async def query_huggingface_api(
    model_url: str, api_key: str, data=None, json_payload=None
) -> dict:
    """
    Generic function to query the Hugging Face API.
    """
    # When API key is not provided, return a small mock response for development/demo mode
    if not api_key:
        # Return a mock caption or embedding depending on payload
        if data is not None:
            # image caption mock
            return {"generated_text": "A demo caption describing the sample image."}
        if json_payload is not None:
            # embedding mock: a deterministic fixed-size vector for demonstration
            return [ [random.random() for _ in range(384)] ]

    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = f"https://api-inference.huggingface.co/models/{model_url}"

    async with httpx.AsyncClient() as client:
        if data:
            response = await client.post(api_url, headers=headers, data=data)
        elif json_payload:
            response = await client.post(api_url, headers=headers, json=json_payload)
        else:
            raise ValueError("Either 'data' or 'json_payload' must be provided.")

        response.raise_for_status()  # Will raise an exception for 4XX/5XX responses
        return response.json()
