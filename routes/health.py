"""Health check and telemetry endpoint."""

from typing import Any

from fastapi import APIRouter

from core.cache import global_aqi_cache, global_geo_cache, global_plan_cache
from core.constants import APP_NAME, APP_VERSION

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, Any]:
    """Return application health status and cache statistics."""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION,
        "cache_stats": {
            "geo": global_geo_cache.stats(),
            "aqi": global_aqi_cache.stats(),
            "plan": global_plan_cache.stats(),
        },
    }
