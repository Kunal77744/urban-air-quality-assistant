"""Air quality service querying Open-Meteo AQI API with memory caching."""

import httpx

from core.cache import global_aqi_cache
from core.constants import (
    AQI_CACHE_TTL_SECONDS,
    AQI_LEVEL_GOOD,
    AQI_LEVEL_MODERATE,
    AQI_LEVEL_POOR,
    AQI_LEVEL_SATISFACTORY,
    AQI_LEVEL_VERY_POOR,
    DEFAULT_HTTP_TIMEOUT,
    OPEN_METEO_AQI_URL,
)
from core.logging import logger
from models.air_quality import AirQualityData


def categorize_aqi(aqi: int) -> tuple[str, str]:
    """Map numeric AQI to descriptive category and advisory."""
    if aqi <= AQI_LEVEL_GOOD:
        return "Good", "Air quality is satisfactory; safe for all activities."
    if aqi <= AQI_LEVEL_SATISFACTORY:
        return "Satisfactory", "Minor breathing discomfort to sensitive people."
    if aqi <= AQI_LEVEL_MODERATE:
        return "Moderate", "Breathing discomfort to people with asthma/heart disease."
    if aqi <= AQI_LEVEL_POOR:
        return "Poor", "Breathing discomfort to most people on prolonged exposure."
    if aqi <= AQI_LEVEL_VERY_POOR:
        return "Very Poor", "Respiratory illness on prolonged exposure."
    return "Severe", "Affects healthy people and seriously impacts sensitive groups."


def _build_fallback_aqi(city: str, lat: float, lon: float) -> AirQualityData:
    """Return realistic fallback AQI when external API is unreachable."""
    category, _ = categorize_aqi(165)
    return AirQualityData(
        city=city,
        latitude=lat,
        longitude=lon,
        aqi=165,
        category=category,
        pm2_5=85.0,
        pm10=140.0,
        source="Estimated Baseline (CPCB Offline)",
        is_fallback=True,
    )


async def get_air_quality(
    city: str,
    lat: float,
    lon: float,
    client: httpx.AsyncClient | None = None,
) -> AirQualityData:
    """Fetch live AQI and PM levels with 30-minute caching."""
    cache_key = f"{round(lat, 2)}_{round(lon, 2)}"
    cached = global_aqi_cache.get(cache_key)
    if cached is not None:
        return cached  # type: ignore[no-any-return]

    params: dict[str, float | list[str]] = {
        "latitude": lat,
        "longitude": lon,
        "current": ["us_aqi", "pm2_5", "pm10"],
    }
    try:
        session = client if client else httpx.AsyncClient()
        async with session:
            resp = await session.get(
                OPEN_METEO_AQI_URL, params=params, timeout=DEFAULT_HTTP_TIMEOUT
            )
            if resp.status_code == 200:
                current = resp.json().get("current", {})
                aqi = int(current.get("us_aqi", 120))
                category, _ = categorize_aqi(aqi)
                data = AirQualityData(
                    city=city,
                    latitude=lat,
                    longitude=lon,
                    aqi=aqi,
                    category=category,
                    pm2_5=float(current.get("pm2_5", 55.0)),
                    pm10=float(current.get("pm10", 90.0)),
                    source="Open-Meteo Live",
                    is_fallback=False,
                )
                global_aqi_cache.set(cache_key, data, AQI_CACHE_TTL_SECONDS)
                return data
    except Exception as err:
        logger.warning("Air quality fetch failed: %s", err)

    return _build_fallback_aqi(city, lat, lon)
