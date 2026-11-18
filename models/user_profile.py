"""User profile input models with strict validation bounds."""

from enum import StrEnum

from pydantic import BaseModel, Field


class CommuteMode(StrEnum):
    """Supported transit modes."""

    CAR = "car"
    CAB = "cab"
    MOTORCYCLE = "motorcycle"
    SCOOTER = "scooter"
    AUTO = "auto"
    BUS = "bus"
    METRO = "metro"
    CYCLE = "cycle"
    WALK = "walk"


class CookingFuel(StrEnum):
    """Household cooking fuel types."""

    INDUCTION = "induction"
    LPG = "lpg"
    BIOMASS = "biomass"
    KEROSENE = "kerosene"


class ExerciseHabit(StrEnum):
    """User exercise habits."""

    MORNING_OUTDOOR = "morning_outdoor"
    EVENING_OUTDOOR = "evening_outdoor"
    INDOOR = "indoor"
    NONE = "none"


class UserProfile(BaseModel):
    """Validated user profile for routine planning."""

    commute_mode: CommuteMode = Field(
        default=CommuteMode.MOTORCYCLE,
        description="Primary mode of daily commuting",
    )
    commute_distance_km: float = Field(
        default=10.0,
        ge=0.0,
        le=150.0,
        description="One-way commute distance in kilometers",
    )
    has_vulnerable_members: bool = Field(
        default=False,
        description="Flag for infants, pregnant women, or elderly at home",
    )
    has_asthma_or_respiratory: bool = Field(
        default=False,
        description="Flag for household members with asthma or COPD",
    )
    work_from_home: bool = Field(
        default=False,
        description="Whether user works remotely",
    )
    cooking_fuel: CookingFuel = Field(
        default=CookingFuel.LPG,
        description="Primary cooking energy source",
    )
    exercise_habit: ExerciseHabit = Field(
        default=ExerciseHabit.MORNING_OUTDOOR,
        description="Primary exercise routine",
    )
