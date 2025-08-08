import httpx
import time
from typing import Optional
from app.core.config import settings

DID_BASE = "https://api.d-id.com/v1"

class DIDClient:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or settings.did_api_key
        if not self.api_key:
            raise RuntimeError("D_ID API key not set")
        self.headers = {"Authorization": f"Basic {self.api_key}"}

    def _client(self) -> httpx.Client:
        return httpx.Client(timeout=60, headers=self.headers)

    def create_talk(self, source_url: str, audio_url: str) -> str:
        payload = {
            "source_url": source_url,
            "script": {"type": "audio", "audio_url": audio_url},
        }
        with self._client() as c:
            r = c.post(f"{DID_BASE}/talks", json=payload)
            r.raise_for_status()
            data = r.json()
            return data["id"]

    def wait_for_result(self, talk_id: str, timeout_s: int = 300) -> str:
        start = time.time()
        with self._client() as c:
            while True:
                r = c.get(f"{DID_BASE}/talks/{talk_id}")
                r.raise_for_status()
                data = r.json()
                status = data.get("status")
                if status == "done":
                    return data["result_url"]
                if status == "error":
                    raise RuntimeError(f"D-ID error: {data}")
                if time.time() - start > timeout_s:
                    raise TimeoutError("D-ID render timed out")
                time.sleep(2)