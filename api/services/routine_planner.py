"""Main personalized routine generation engine."""

from models.air_quality import AirQualityData
from models.routine_plan import RoutinePlanResponse, SustainableAlternative
from models.user_profile import CommuteMode, CookingFuel, UserProfile
from services.impact_engine import build_impact_summary, calculate_commute_co2_savings
from services.planner_helpers import generate_indoor_hacks, generate_time_routines


def _determine_commute_alt(mode: CommuteMode) -> tuple[str, str, str]:
    """Map user's current commute to the best green alternative."""
    if mode in (CommuteMode.CAR, CommuteMode.CAB):
        return (
            "metro",
            "Metro Rail / Carpool",
            "Cuts private car exhaust and traffic congestion",
        )
    if mode in (CommuteMode.MOTORCYCLE, CommuteMode.SCOOTER):
        return (
            "bus",
            "Electric / CNG City Bus",
            "Reduces direct street-level tailpipe inhalation",
        )
    if mode == CommuteMode.AUTO:
        return (
            "metro",
            "Metro Rail / Shared Transit",
            "Eliminates high 2-stroke emissions",
        )
    return "walk", "Walking / Cycling", "Zero-emission physical active travel"


def _build_commute_alternative(
    profile: UserProfile, is_hi: bool
) -> SustainableAlternative:
    """Create commute alternative item."""
    alt_mode, alt_name, why_commute = _determine_commute_alt(profile.commute_mode)
    savings = calculate_commute_co2_savings(
        profile.commute_mode.value, alt_mode, profile.commute_distance_km
    )
    return SustainableAlternative(
        category="commute",
        current_practice=f"{profile.commute_mode.value.title()} ({profile.commute_distance_km} km)",
        suggested_alternative="मेट्रो या इलेक्ट्रिक बस" if is_hi else alt_name,
        co2_saved_grams_per_day=savings,
        why_explanation="सड़क पर उत्सर्जन और धुंध को सीधे कम करता है।"
        if is_hi
        else why_commute,
    )


def _build_fuel_alternative(fuel: CookingFuel, is_hi: bool) -> SustainableAlternative:
    """Create clean cooking fuel alternative item."""
    return SustainableAlternative(
        category="cooking_fuel",
        current_practice=fuel.value.title(),
        suggested_alternative="इंडक्शन चूल्हा / एलपीजी"
        if is_hi
        else "Induction Cooktop / LPG",
        co2_saved_grams_per_day=450.0,
        why_explanation="बायोमास धुआं फेफड़ों को भारी नुकसान पहुंचाता है।"
        if is_hi
        else "Biomass releases high carbon monoxide & black carbon indoors.",
    )


def generate_alternatives(
    profile: UserProfile, is_hi: bool
) -> list[SustainableAlternative]:
    """Generate sustainable alternatives tailored to user's lifestyle."""
    items = [_build_commute_alternative(profile, is_hi)]
    if profile.cooking_fuel in (CookingFuel.BIOMASS, CookingFuel.KEROSENE):
        items.append(_build_fuel_alternative(profile.cooking_fuel, is_hi))
    return items


def create_routine_plan(
    aqi_data: AirQualityData,
    profile: UserProfile,
    language: str = "en",
) -> RoutinePlanResponse:
    """Generate complete personalized plan with deterministic impact."""
    is_hi = language.lower() == "hi"
    routines = generate_time_routines(aqi_data, profile, is_hi)
    indoor_hacks = generate_indoor_hacks(is_hi)
    alternatives = generate_alternatives(profile, is_hi)

    alt_mode, _, _ = _determine_commute_alt(profile.commute_mode)
    impact = build_impact_summary(
        current_mode=profile.commute_mode.value,
        alternative_mode=alt_mode,
        commute_distance_km=profile.commute_distance_km,
    )

    return RoutinePlanResponse(
        air_quality=aqi_data,
        routines=routines,
        indoor_hacks=indoor_hacks,
        alternatives=alternatives,
        impact=impact,
    )
