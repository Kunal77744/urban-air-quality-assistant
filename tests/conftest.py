"""Pytest fixtures, mock HTTP clients, and test configurations."""

from collections.abc import Generator
from unittest.mock import patch

import httpx
import pytest
from fastapi.testclient import TestClient

from core.cache import global_aqi_cache, global_geo_cache, global_plan_cache
from core.security import _request_timestamps
from main import app
from models.air_quality import AirQualityData
from models.user_profile import CommuteMode, CookingFuel, ExerciseHabit, UserProfile

GEO_PAYLOAD = {
    "results": [
        {
            "name": "Delhi",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "country": "India",
            "admin1": "Delhi",
        }
    ]
}

AQI_PAYLOAD = {
    "current": {
        "us_aqi": 185,
        "pm2_5": 75.0,
        "pm10": 130.0,
    }
}


@pytest.fixture(autouse=True)
def clear_caches_and_mock_http() -> Generator[None, None, None]:
    """Ensure clean cache state and mock external HTTP calls before each test."""
    global_geo_cache.clear()
    global_aqi_cache.clear()
    global_plan_cache.clear()
    _request_timestamps.clear()

    async def mock_get(
        self: httpx.AsyncClient, url: str, **kwargs: object
    ) -> httpx.Response:
        _ = kwargs
        url_str = str(url)
        req = httpx.Request("GET", url)
        if "geocoding" in url_str:
            return httpx.Response(200, json=GEO_PAYLOAD, request=req)
        return httpx.Response(200, json=AQI_PAYLOAD, request=req)

    with patch.object(httpx.AsyncClient, "get", new=mock_get):
        yield

    global_geo_cache.clear()
    global_aqi_cache.clear()
    global_plan_cache.clear()
    _request_timestamps.clear()


@pytest.fixture
def client() -> TestClient:
    """Synchronous test client for route testing."""
    return TestClient(app)


@pytest.fixture
def sample_profile() -> UserProfile:
    """Standard urban commuter profile."""
    return UserProfile(
        commute_mode=CommuteMode.CAR,
        commute_distance_km=15.0,
        has_vulnerable_members=False,
        has_asthma_or_respiratory=False,
        work_from_home=False,
        cooking_fuel=CookingFuel.LPG,
        exercise_habit=ExerciseHabit.MORNING_OUTDOOR,
    )


@pytest.fixture
def sample_aqi() -> AirQualityData:
    """Standard poor AQI scenario for Delhi."""
    return AirQualityData(
        city="New Delhi",
        latitude=28.6139,
        longitude=77.2090,
        aqi=245,
        category="Poor",
        pm2_5=120.0,
        pm10=210.0,
        source="Open-Meteo Test",
        is_fallback=False,
    )
