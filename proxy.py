"""
Implement a Proxy for the slow RealVideoService that provides:
- Lazy loading: do NOT construct the real service until it's actually needed.
- Caching: cache results of download_compressed(video_id, quality).
"""
from __future__ import annotations
from typing import Callable, Dict, Tuple, Optional

# NOTE: We only import the class name to use it as a type. The tests may supply
# their own fake service via the factory.
from video_service import RealVideoService

class ProxyVideoService:
    def __init__(self, service_factory: Callable[[], RealVideoService]) -> None:
        """
        Initialize the proxy with a factory that can build the real service.
        Do NOT call the factory here (lazy construction!).
        """

        # TODO: store the factory, set the underlying service to None,
        # and initialize an in-memory cache (e.g., a dict).
        self.factory = service_factory
        self.service: Optional[RealVideoService] = None
        self.cache = {}
        self.MAX_SIZE = 10
        self.cache_hit = 0
        self.cache_miss = 0

    def _ensure_service(self) -> RealVideoService:
        """Construct the real service on demand (only when needed)."""
        # TODO: if we don't have a real service yet, call the factory and store it.
        # Then, return the real service.

        if not self.service:
            self.service = self.factory()
        return self.service

    def download_compressed(self, video_id: str, quality: str) -> bytes:
        """Return compressed bytes for (video_id, quality), using a cache."""
        # TODO:
        # 1) Create a cache key (video_id, quality).
        # 2) If present in cache, return it directly.
        # 3) Otherwise, ensure the service exists, call its download_compressed,
        #    store the result in cache, and return it.

        if (video_id, quality) in self.cache:
            self.cache_hit += 1
            print(f"Cache hit: {self.cache_hit}/{self.cache_hit+self.cache_miss}")
            return self.cache[video_id, quality]
        else:
            self.cache_miss += 1
            if not self.service:
                self._ensure_service()
            compressed_vid = self.service.download_compressed(video_id, quality)
            if len(self.cache) < self.MAX_SIZE:
                self.cache[(video_id, quality)] = compressed_vid
                
            print(f"Cache miss: {self.cache_hit}/{self.cache_hit+self.cache_miss}")
            return compressed_vid
