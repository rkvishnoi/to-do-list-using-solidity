import httpx
from app.core.config import settings

ELEVEN_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"

async def tts_preview_bytes(text: str, voice_id: str | None = None, model_id: str = "eleven_multilingual_v2") -> bytes:
    if not settings.elevenlabs_api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")
    voice = voice_id or settings.elevenlabs_default_voice_id
    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(f"{ELEVEN_TTS_URL}/{voice}", json=payload, headers=headers)
        resp.raise_for_status()
        return resp.content