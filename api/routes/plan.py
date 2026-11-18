"""Personalized clean air routine plan generation route."""

from fastapi import APIRouter

from core.cache import global_plan_cache
from core.constants import (
    FALLBACK_CITY,
    FALLBACK_LAT,
    FALLBACK_LON,
    PLAN_CACHE_TTL_SECONDS,
)
from models.air_quality import AirQualityData
from models.routine_plan import RoutinePlanRequest, RoutinePlanResponse
from services.aqi_service import get_air_quality
from services.geocoding_service import search_locations
from services.llm_service import enrich_plan_with_llm
from services.routine_planner import create_routine_plan

router = APIRouter()


async def _resolve_coords(req: RoutinePlanRequest) -> tuple[str, float, float]:
    """Resolve latitude and longitude from request or geocoding."""
    if req.latitude is not None and req.longitude is not None:
        return req.city, req.latitude, req.longitude
    locations = await search_locations(req.city)
    if locations:
        loc = locations[0]
        return loc.name, loc.latitude, loc.longitude
    return FALLBACK_CITY, FALLBACK_LAT, FALLBACK_LON


@router.post("/generate", response_model=RoutinePlanResponse)
async def generate_plan(req: RoutinePlanRequest) -> RoutinePlanResponse:
    """Generate tailored low-emission routines and verified impact."""
    cache_key = f"{req.city}_{req.profile.commute_mode.value}_{req.language}"
    cached = global_plan_cache.get(cache_key)
    if cached is not None:
        return cached  # type: ignore[no-any-return]

    city, lat, lon = await _resolve_coords(req)
    aqi_data: AirQualityData = await get_air_quality(city=city, lat=lat, lon=lon)
    plan = create_routine_plan(aqi_data, req.profile, language=req.language)
    enriched_plan = await enrich_plan_with_llm(plan)

    global_plan_cache.set(cache_key, enriched_plan, PLAN_CACHE_TTL_SECONDS)
    return enriched_plan
