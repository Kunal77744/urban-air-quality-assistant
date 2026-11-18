"""Air quality measurement route."""

from fastapi import APIRouter, Query

from models.air_quality import AirQualityData
from services.aqi_service import get_air_quality

router = APIRouter()


@router.get("/live", response_model=AirQualityData)
async def live_air_quality(
    city: str = Query(default="New Delhi", min_length=1, max_length=100),
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
) -> AirQualityData:
    """Fetch current AQI and pollutant concentrations for coordinates."""
    return await get_air_quality(city=city, lat=lat, lon=lon)
