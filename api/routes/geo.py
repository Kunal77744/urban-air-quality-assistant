"""Geographical location search route."""

from fastapi import APIRouter, Query

from models.air_quality import GeoLocation
from services.geocoding_service import search_locations

router = APIRouter()


@router.get("/search", response_model=list[GeoLocation])
async def search_cities(
    q: str = Query(..., min_length=1, max_length=100, description="City name query"),
) -> list[GeoLocation]:
    """Search matching global cities with geocoordinates."""
    return await search_locations(q)
