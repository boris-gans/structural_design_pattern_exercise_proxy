import time
import types
import pytest

from proxy import ProxyVideoService

class FakeVideoService:
    """A controllable fake that counts factory calls and compress calls."""
    def __init__(self, compress_seconds: float = 0.0):
        self.compress_seconds = compress_seconds
        self.compress_calls = 0

    def download_compressed(self, video_id: str, quality: str) -> bytes:
        self.compress_calls += 1
        time.sleep(self.compress_seconds)
        return f"FAKE:{video_id}|Q:{quality}".encode("utf-8")


def test_does_not_construct_service_until_needed(monkeypatch):
    # Track when the factory is called
    calls = {"count": 0}
    def factory():
        calls["count"] += 1
        return FakeVideoService()

    proxy = ProxyVideoService(service_factory=factory)
    # Lazy: factory should not be called on construction
    assert calls["count"] == 0

    # First actual use triggers construction
    data = proxy.download_compressed("abc", "720p")
    assert data == b"FAKE:abc|Q:720p"
    assert calls["count"] == 1

    # Cached second call should NOT construct a new real service
    again = proxy.download_compressed("abc", "720p")
    assert again == b"FAKE:abc|Q:720p"
    assert calls["count"] == 1  # still 1


def test_caches_by_video_and_quality(monkeypatch):
    def factory():
        return FakeVideoService()

    proxy = ProxyVideoService(service_factory=factory)

    first = proxy.download_compressed("movie1", "1080p")
    # Different quality => cache miss, should call the service again
    second = proxy.download_compressed("movie1", "720p")
    assert first != second

    # Same pair should be cached
    again = proxy.download_compressed("movie1", "720p")
    assert again == second


def test_cache_avoids_repeating_slow_work(monkeypatch):
    # Simulate slowness but keep the suite fast by monkeypatching time.sleep
    monkeypatch.setattr(time, "sleep", lambda s: None)

    svc = FakeVideoService(compress_seconds=1.0)
    def factory():
        return svc

    proxy = ProxyVideoService(service_factory=factory)

    a = proxy.download_compressed("vid42", "480p")
    b = proxy.download_compressed("vid42", "480p")
    assert a == b

    # The real service should have compressed only once because of caching
    assert svc.compress_calls == 1


def test_still_delegates_on_cache_miss(monkeypatch):
    svc = FakeVideoService()
    def factory():
        return svc

    proxy = ProxyVideoService(service_factory=factory)

    out = proxy.download_compressed("x", "360p")
    assert out == b"FAKE:x|Q:360p"
    assert svc.compress_calls == 1
