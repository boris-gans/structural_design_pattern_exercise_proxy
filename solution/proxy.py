from __future__ import annotations
from typing import Callable, Dict, Tuple, Optional
from video_service import RealVideoService

class ProxyVideoService:
    def __init__(self, service_factory: Callable[[], RealVideoService]) -> None:
        self._factory: Callable[[], RealVideoService] = service_factory
        self._service: Optional[RealVideoService] = None
        self._cache: Dict[Tuple[str, str], bytes] = {}

    def _ensure_service(self) -> RealVideoService:
        if self._service is None:
            self._service = self._factory()
        return self._service

    def download_compressed(self, video_id: str, quality: str) -> bytes:
        key = (video_id, quality)
        if key in self._cache:
            return self._cache[key]
        service = self._ensure_service()
        data = service.download_compressed(video_id, quality)
        self._cache[key] = data
        return data
