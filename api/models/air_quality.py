"""Data models representing geocoding and air quality metrics."""

from pydantic import BaseModel, Field


class GeoLocation(BaseModel):
    """Geocoded geographical coordinates."""

    name: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    country: str | None = Field(default=None, max_length=100)
    admin1: str | None = Field(default=None, max_length=100)


class AirQualityData(BaseModel):
    """Air quality index and pollutant measurements."""

    city: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    aqi: int = Field(..., ge=0, le=1000, description="US EPA / CPCB normalized AQI")
    category: str = Field(..., description="Good, Moderate, Poor, Severe, etc.")
    pm2_5: float = Field(..., ge=0.0, le=2000.0, description="PM2.5 in ug/m3")
    pm10: float = Field(..., ge=0.0, le=3000.0, description="PM10 in ug/m3")
    source: str = Field(default="Open-Meteo", description="Data source attribution")
    is_fallback: bool = Field(default=False, description="True if mock fallback used")
