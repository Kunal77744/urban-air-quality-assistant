"""Models for daily routines, indoor hacks, and impact estimates."""

from pydantic import BaseModel, Field

from models.air_quality import AirQualityData
from models.user_profile import UserProfile


class RoutineItem(BaseModel):
    """Specific routine action scheduled for a time slot."""

    slot: str = Field(..., description="morning, afternoon, or evening")
    action: str = Field(..., max_length=200)
    why: str = Field(..., max_length=300)
    exposure_impact: str = Field(..., max_length=100)


class IndoorHack(BaseModel):
    """Actionable hack for indoor air pollution reduction."""

    category: str = Field(..., description="ventilation, filtration, cooking, cleaning")
    title: str = Field(..., max_length=120)
    description: str = Field(..., max_length=350)
    fact_check: str | None = Field(default=None, max_length=250)


class SustainableAlternative(BaseModel):
    """Low-emission alternative to user current baseline habit."""

    category: str = Field(..., description="commute, energy, heating")
    current_practice: str = Field(..., max_length=150)
    suggested_alternative: str = Field(..., max_length=150)
    co2_saved_grams_per_day: float = Field(..., ge=0.0)
    why_explanation: str = Field(..., max_length=300)


class ImpactSummary(BaseModel):
    """Deterministic quantified impact of recommended choices."""

    daily_co2_saved_grams: float = Field(..., ge=0.0)
    annual_co2_saved_kg: float = Field(..., ge=0.0)
    exposure_reduction_pct: float = Field(..., ge=0.0, le=100.0)
    calculation_basis: str = Field(..., max_length=400)
    disclaimer: str = Field(
        default="Estimated based on ARAI/CPCB factors and WHO exposure reduction models.",
        max_length=200,
    )


class RoutinePlanRequest(BaseModel):
    """Request payload to generate personalized plan."""

    city: str = Field(default="New Delhi", min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90.0, le=90.0)
    longitude: float | None = Field(default=None, ge=-180.0, le=180.0)
    profile: UserProfile = Field(default_factory=UserProfile)
    language: str = Field(default="en", pattern="^(en|hi)$")


class RoutinePlanResponse(BaseModel):
    """Comprehensive personalized routine, hacks, and verified impact."""

    air_quality: AirQualityData
    routines: list[RoutineItem]
    indoor_hacks: list[IndoorHack]
    alternatives: list[SustainableAlternative]
    impact: ImpactSummary
