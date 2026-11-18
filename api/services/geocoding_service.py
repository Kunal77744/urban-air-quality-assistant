"""Geocoding service fetching coordinates via Open-Meteo with caching."""

from typing import Any

import httpx

from core.cache import global_geo_cache
from core.constants import (
    DEFAULT_HTTP_TIMEOUT,
    FALLBACK_CITY,
    FALLBACK_LAT,
    FALLBACK_LON,
    GEO_CACHE_TTL_SECONDS,
    OPEN_METEO_GEO_URL,
)
from core.logging import logger
from models.air_quality import GeoLocation


def _get_fallback_locations(query: str) -> list[GeoLocation]:
    """Provide static fallback when geocoding network fails."""
    return [
        GeoLocation(
            name=query.title() if query else FALLBACK_CITY,
            latitude=FALLBACK_LAT,
            longitude=FALLBACK_LON,
            country="India",
            admin1="Delhi",
        )
    ]


def _parse_geo_results(data: dict[str, Any], query: str) -> list[GeoLocation]:
    """Transform Open-Meteo payload into GeoLocation models."""
    return [
        GeoLocation(
            name=item.get("name", query.title()),
            latitude=float(item.get("latitude", FALLBACK_LAT)),
            longitude=float(item.get("longitude", FALLBACK_LON)),
            country=item.get("country"),
            admin1=item.get("admin1"),
        )
        for item in data.get("results", [])
    ]


async def _fetch_geo_data(
    clean_query: str, client: httpx.AsyncClient | None
) -> dict[str, Any]:
    """Fetch JSON from Open-Meteo geocoding endpoint."""
    params: dict[str, str | int] = {"name": clean_query, "count": 5, "format": "json"}
    if client:
        resp = await client.get(
            OPEN_METEO_GEO_URL, params=params, timeout=DEFAULT_HTTP_TIMEOUT
        )
    else:
        async with httpx.AsyncClient() as session:
            resp = await session.get(
                OPEN_METEO_GEO_URL, params=params, timeout=DEFAULT_HTTP_TIMEOUT
            )
    return resp.json() if resp.status_code == 200 else {}


async def search_locations(
    query: str,
    client: httpx.AsyncClient | None = None,
) -> list[GeoLocation]:
    """Search for matching city coordinates with memory caching."""
    clean_query = query.strip().lower()
    if not clean_query:
        return []

    cached = global_geo_cache.get(clean_query)
    if cached is not None:
        return cached  # type: ignore[no-any-return]

    try:
        data = await _fetch_geo_data(clean_query, client)
        results = _parse_geo_results(data, clean_query)
        if results:
            global_geo_cache.set(clean_query, results, GEO_CACHE_TTL_SECONDS)
            return results
    except Exception as err:
        logger.warning("Geocoding fetch failed for '%s': %s", clean_query, err)

    return _get_fallback_locations(clean_query)
