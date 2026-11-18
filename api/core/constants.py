"""Application-wide constants, emission baselines, and AQI thresholds.

All factors are derived from ARAI, CPCB, and WHO air quality guidelines.
"""

from collections.abc import Mapping
from typing import Final

# Application Metadata
APP_NAME: Final[str] = "Urban Air Quality Assistant"
APP_VERSION: Final[str] = "1.0.0"

# Cache TTL Configuration (in seconds)
GEO_CACHE_TTL_SECONDS: Final[int] = 86400  # 24 hours
AQI_CACHE_TTL_SECONDS: Final[int] = 1800  # 30 minutes
PLAN_CACHE_TTL_SECONDS: Final[int] = 900  # 15 minutes
MAX_CACHE_ENTRIES: Final[int] = 1024

# External API Configuration
OPEN_METEO_GEO_URL: Final[str] = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_AQI_URL: Final[str] = "https://air-quality-api.open-meteo.com/v1/air-quality"
DEFAULT_HTTP_TIMEOUT: Final[float] = 6.0

# Transport Emission Factors (g CO2 per passenger-km)
# Sources: ARAI (Automotive Research Association of India) & CPCB baselines
EMISSION_FACTORS: Final[Mapping[str, float]] = {
    "car": 140.0,
    "cab": 140.0,
    "motorcycle": 42.0,
    "scooter": 42.0,
    "auto": 55.0,
    "bus": 18.0,
    "metro": 8.0,
    "cycle": 0.0,
    "walk": 0.0,
}

# Air Quality Thresholds & Exposure Modifiers
AQI_LEVEL_GOOD: Final[int] = 50
AQI_LEVEL_SATISFACTORY: Final[int] = 100
AQI_LEVEL_MODERATE: Final[int] = 200
AQI_LEVEL_POOR: Final[int] = 300
AQI_LEVEL_VERY_POOR: Final[int] = 400

# Indoor Air Efficiency Reductions (0.0 to 1.0)
VENT_TIMING_REDUCTION: Final[float] = 0.30
HEPA_PURIFIER_REDUCTION: Final[float] = 0.75
COOKING_VENT_REDUCTION: Final[float] = 0.60
WET_CLEANING_REDUCTION: Final[float] = 0.35

# Default Safe Fallback Location (New Delhi)
FALLBACK_CITY: Final[str] = "New Delhi"
FALLBACK_LAT: Final[float] = 28.6139
FALLBACK_LON: Final[float] = 77.2090
