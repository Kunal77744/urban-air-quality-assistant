"""Integration tests for all FastAPI endpoints (Requirements R1-R7)."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    """Verify health status and telemetry payload."""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "cache_stats" in data


def test_geo_search_endpoint(client: TestClient) -> None:
    """Verify city search returns geocoordinates."""
    resp = client.get("/api/geo/search?q=Mumbai")
    assert resp.status_code == 200
    results = resp.json()
    assert isinstance(results, list)
    assert len(results) > 0
    assert "latitude" in results[0]
    assert "longitude" in results[0]


def test_live_aqi_endpoint(client: TestClient) -> None:
    """Verify live AQI retrieval with coordinates."""
    resp = client.get("/api/aqi/live?city=Delhi&lat=28.61&lon=77.20")
    assert resp.status_code == 200
    data = resp.json()
    assert data["city"] == "Delhi"
    assert "aqi" in data
    assert "pm2_5" in data


def test_plan_generate_full_flow(client: TestClient) -> None:
    """Verify complete end-to-end plan generation."""
    payload = {
        "city": "Bengaluru",
        "profile": {
            "commute_mode": "car",
            "commute_distance_km": 12.0,
            "has_vulnerable_members": True,
            "has_asthma_or_respiratory": False,
            "cooking_fuel": "lpg",
            "exercise_habit": "indoor",
        },
        "language": "en",
    }
    resp = client.post("/api/plan/generate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "air_quality" in data
    assert len(data["routines"]) == 3
    assert len(data["indoor_hacks"]) >= 4
    assert len(data["alternatives"]) >= 1
    assert data["impact"]["daily_co2_saved_grams"] > 0
