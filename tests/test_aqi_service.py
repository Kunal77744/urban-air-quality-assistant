"""Tests for geocoding and live air quality service (Requirement R1)."""

import pytest

from core.cache import global_aqi_cache, global_geo_cache
from services.aqi_service import categorize_aqi, get_air_quality
from services.geocoding_service import search_locations


@pytest.mark.asyncio
async def test_geocoding_fallback_on_empty() -> None:
    """Empty query should return empty list."""
    res = await search_locations("")
    assert res == []


@pytest.mark.asyncio
async def test_geocoding_caching() -> None:
    """Second call should return from cache without network request."""
    res1 = await search_locations("Delhi")
    assert len(res1) > 0
    stats_before = global_geo_cache.stats()
    res2 = await search_locations("Delhi")
    assert res1 == res2
    stats_after = global_geo_cache.stats()
    assert stats_after["hits"] == stats_before["hits"] + 1


@pytest.mark.asyncio
async def test_air_quality_cache_hit_proven() -> None:
    """Verify AQI cache records hit on repeated coordinate lookup."""
    aqi1 = await get_air_quality("Delhi", 28.61, 77.20)
    assert aqi1.aqi >= 0
    stats1 = global_aqi_cache.stats()
    aqi2 = await get_air_quality("Delhi", 28.61, 77.20)
    assert aqi1.city == aqi2.city
    stats2 = global_aqi_cache.stats()
    assert stats2["hits"] == stats1["hits"] + 1


@pytest.mark.parametrize(
    "aqi,expected_category",
    [
        (30, "Good"),
        (85, "Satisfactory"),
        (150, "Moderate"),
        (250, "Poor"),
        (350, "Very Poor"),
        (450, "Severe"),
    ],
)
def test_categorize_aqi_thresholds(aqi: int, expected_category: str) -> None:
    """Validate standard CPCB/EPA AQI category boundaries."""
    category, _ = categorize_aqi(aqi)
    assert category == expected_category
