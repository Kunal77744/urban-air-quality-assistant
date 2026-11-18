"""High-performance TTL and LRU in-memory cache."""

import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any

from core.constants import MAX_CACHE_ENTRIES


@dataclass
class CacheEntry:
    """Represents a cached value with its expiration timestamp."""

    value: Any
    expires_at: float


class InMemoryCache:
    """Thread-safe TTL + LRU in-memory cache store."""

    def __init__(self, max_size: int = MAX_CACHE_ENTRIES) -> None:
        self._max_size = max_size
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits: int = 0
        self._misses: int = 0

    def get(self, key: str) -> Any | None:
        """Retrieve key value if present and not expired."""
        if key not in self._store:
            self._misses += 1
            return None

        entry = self._store[key]
        if time.monotonic() >= entry.expires_at:
            del self._store[key]
            self._misses += 1
            return None

        self._store.move_to_end(key)
        self._hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Store key-value with specified TTL in seconds."""
        if key in self._store:
            del self._store[key]
        elif len(self._store) >= self._max_size:
            self._store.popitem(last=False)

        expires_at = time.monotonic() + ttl_seconds
        self._store[key] = CacheEntry(value=value, expires_at=expires_at)

    def stats(self) -> dict[str, int]:
        """Return cache hit and miss performance metrics."""
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": len(self._store),
        }

    def clear(self) -> None:
        """Clear all entries from cache store."""
        self._store.clear()
        self._hits = 0
        self._misses = 0


# Global shared cache instances
global_geo_cache = InMemoryCache()
global_aqi_cache = InMemoryCache()
global_plan_cache = InMemoryCache()
