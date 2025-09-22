# Proxy Pattern Exercise

You are asked to implement a **Proxy** for a slow video service. The proxy must:

- **Lazy-load** the real service (do not create it until actually needed).
- **Cache** compressed downloads per `(video_id, quality)` so repeated requests are instant and **do not** hit the real service again.

## Scenario

`RealVideoService` is slow to **start up** and slow to **compress** videos for download. We provide a proxy interface placeholder in `proxy.py` that you must implement.

The tests in `tests/test_proxy.py` verify:

1. The proxy does **not** construct the real service until a method is actually called.
2. The proxy **caches** compressed results and avoids calling the real service again for the same `(video_id, quality)`.
3. Different qualities are **not** mixed up in the cache.
4. The proxy can still delegate to the real service when the cache misses.

> The real service uses `time.sleep` to simulate slowness. Tests monkeypatch it so the suite runs fast.

## Files

- `video_service.py` — contains the `RealVideoService` used by the proxy and a small interface note.
- `proxy.py` — **YOU IMPLEMENT THIS**. Follow the TODOs.
- `tests/test_proxy.py` — pytest tests that validate your solution.

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## What to implement

In `proxy.py`, implement `ProxyVideoService` such that:

- It accepts a **factory** callable `service_factory` that constructs the real service **only when needed**.
- `download_compressed(video_id: str, quality: str) -> bytes`:
  - On first request for a given `(video_id, quality)`, construct the real service (if not already created), delegate to it, store the result in an internal cache, and return it.
  - On subsequent requests for the same pair, return the cached bytes **without** calling the real service again.

### Extra goals

- Add a `maxsize` to the cache (LRU).
- Add simple metrics: cache hits/misses.
