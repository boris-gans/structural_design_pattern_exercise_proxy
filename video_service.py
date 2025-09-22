"""
A tiny "video service" that simulates an expensive startup and a slow compression step.
Your Proxy will wrap this service and add lazy loading + caching.

We keep the interface intentionally small:
- download_compressed(video_id: str, quality: str) -> bytes
"""
from __future__ import annotations
import time
from typing import Optional

class RealVideoService:
    def __init__(self, startup_seconds: float = 2.0, compress_seconds: float = 1.5) -> None:
        time.sleep(startup_seconds)
        self._startup_seconds = startup_seconds
        self._compress_seconds = compress_seconds

    def download_compressed(self, video_id: str, quality: str) -> bytes:
        """Simulate slow compression and return some bytes for the download."""
        time.sleep(self._compress_seconds)
        payload = f"VIDEO:{video_id}|Q:{quality}".encode("utf-8")
        return payload
