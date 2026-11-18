"""Tests for error handlers, exceptions, and cache expiration."""

import time

import pytest
from starlette.requests import Request

from core.cache import InMemoryCache
from core.errors import (
    AppException,
    ExternalAPIError,
    LocationNotFoundError,
    app_exception_handler,
    generic_exception_handler,
)


def test_custom_exceptions() -> None:
    """Validate status codes and messages of domain exceptions."""
    app_err = AppException("Generic error", status_code=500)
    assert app_err.status_code == 500

    ext_err = ExternalAPIError("OpenMeteo", "timeout")
    assert ext_err.status_code == 502

    loc_err = LocationNotFoundError("Atlantis")
    assert loc_err.status_code == 404
    assert "Atlantis" in loc_err.message


@pytest.mark.asyncio
async def test_exception_handlers() -> None:
    """Test custom and generic JSON error handlers."""
    scope = {"type": "http", "method": "GET", "path": "/"}
    req = Request(scope)

    resp1 = await app_exception_handler(req, AppException("Custom error", 400))
    assert resp1.status_code == 400

    resp2 = await generic_exception_handler(req, RuntimeError("Unexpected error"))
    assert resp2.status_code == 500


def test_cache_ttl_expiration() -> None:
    """Verify that cached entries expire after their TTL."""
    cache = InMemoryCache(max_size=2)
    cache.set("key1", "val1", ttl_seconds=0)
    time.sleep(0.01)
    assert cache.get("key1") is None


def test_cache_lru_eviction() -> None:
    """Verify LRU item eviction when capacity is exceeded."""
    cache = InMemoryCache(max_size=2)
    cache.set("a", 1, ttl_seconds=100)
    cache.set("b", 2, ttl_seconds=100)
    cache.set("c", 3, ttl_seconds=100)
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3
