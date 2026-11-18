"""Tests for routine planner and hacks generation (Requirements R2, R3, R4, R5)."""

from models.air_quality import AirQualityData
from models.user_profile import CommuteMode, CookingFuel, ExerciseHabit, UserProfile
from services.routine_planner import create_routine_plan


def test_routine_planner_poor_aqi_vulnerable(sample_aqi: AirQualityData) -> None:
    """High risk profile under poor AQI should receive indoor workout advice."""
    profile = UserProfile(
        commute_mode=CommuteMode.CAR,
        commute_distance_km=12.0,
        has_asthma_or_respiratory=True,
        exercise_habit=ExerciseHabit.MORNING_OUTDOOR,
    )
    plan = create_routine_plan(sample_aqi, profile, language="en")
    assert len(plan.routines) == 3
    morning = plan.routines[0]
    assert morning.slot == "morning"
    assert "indoor" in morning.action.lower()


def test_routine_planner_hindi_localization(sample_aqi: AirQualityData) -> None:
    """Hindi language toggle should provide translated recommendations."""
    profile = UserProfile(commute_mode=CommuteMode.MOTORCYCLE)
    plan = create_routine_plan(sample_aqi, profile, language="hi")
    assert any("व्यायाम" in r.action or "खिड़कियां" in r.action for r in plan.routines)
    assert any("वेंटिलेशन" in h.title for h in plan.indoor_hacks)


def test_indoor_hacks_content(
    sample_aqi: AirQualityData, sample_profile: UserProfile
) -> None:
    """Verify all four R4 indoor hacks and plant myth-buster are generated."""
    plan = create_routine_plan(sample_aqi, sample_profile, language="en")
    categories = [h.category for h in plan.indoor_hacks]
    assert "ventilation" in categories
    assert "filtration" in categories
    assert "cooking" in categories
    assert "cleaning" in categories
    myth = next(h for h in plan.indoor_hacks if h.category == "cleaning")
    assert myth.fact_check is not None
    assert "Houseplants" in myth.fact_check


def test_sustainable_alternatives_cooking_fuel(sample_aqi: AirQualityData) -> None:
    """Biomass fuel should trigger induction stove recommendation."""
    profile = UserProfile(
        commute_mode=CommuteMode.SCOOTER,
        cooking_fuel=CookingFuel.BIOMASS,
    )
    plan = create_routine_plan(sample_aqi, profile, language="en")
    alt_categories = [a.category for a in plan.alternatives]
    assert "cooking_fuel" in alt_categories
    fuel_alt = next(a for a in plan.alternatives if a.category == "cooking_fuel")
    assert "Induction" in fuel_alt.suggested_alternative
