"""Deterministic emissions and personal exposure reduction calculation engine.

Strictly deterministic: zero random numbers, zero LLM hallucinations.
Formulas based on ARAI emission baselines and WHO exposure guidelines.
"""

from core.constants import (
    COOKING_VENT_REDUCTION,
    EMISSION_FACTORS,
    HEPA_PURIFIER_REDUCTION,
    VENT_TIMING_REDUCTION,
    WET_CLEANING_REDUCTION,
)
from models.routine_plan import ImpactSummary


def get_emission_factor(mode: str) -> float:
    """Return grams of CO2 per km for a given transit mode."""
    return EMISSION_FACTORS.get(mode.lower(), 42.0)


def calculate_commute_co2_savings(
    current_mode: str,
    alternative_mode: str,
    distance_km: float,
) -> float:
    """Compute roundtrip daily grams of CO2 saved by switching commute mode."""
    factor_curr = get_emission_factor(current_mode)
    factor_alt = get_emission_factor(alternative_mode)
    savings_per_km = max(0.0, factor_curr - factor_alt)
    roundtrip_km = distance_km * 2.0
    return round(savings_per_km * roundtrip_km, 1)


def calculate_exposure_reduction_pct(
    use_vent_timing: bool = True,
    use_purifier_or_filter: bool = True,
    use_cooking_exhaust: bool = True,
    use_wet_cleaning: bool = True,
) -> float:
    """Compute combined percentage reduction in indoor PM2.5 exposure."""
    mult = 1.0
    if use_vent_timing:
        mult *= 1.0 - VENT_TIMING_REDUCTION
    if use_purifier_or_filter:
        mult *= 1.0 - HEPA_PURIFIER_REDUCTION
    if use_cooking_exhaust:
        mult *= 1.0 - COOKING_VENT_REDUCTION
    if use_wet_cleaning:
        mult *= 1.0 - WET_CLEANING_REDUCTION
    return min(95.0, round((1.0 - mult) * 100.0, 1))


def _format_impact_basis(curr: str, alt: str, km: float) -> str:
    """Format emission calculation explanation string."""
    f_curr = get_emission_factor(curr)
    f_alt = get_emission_factor(alt)
    return (
        f"CO2 savings calculated using ARAI baseline: "
        f"{curr} ({f_curr}g/km) vs {alt} ({f_alt}g/km) "
        f"over {km * 2:.1f} km roundtrip."
    )


def build_impact_summary(
    current_mode: str,
    alternative_mode: str,
    commute_distance_km: float,
    working_days_per_year: int = 250,
) -> ImpactSummary:
    """Produce deterministic verified impact summary."""
    daily_g = calculate_commute_co2_savings(
        current_mode, alternative_mode, commute_distance_km
    )
    annual_kg = round((daily_g * working_days_per_year) / 1000.0, 1)
    basis = _format_impact_basis(current_mode, alternative_mode, commute_distance_km)

    return ImpactSummary(
        daily_co2_saved_grams=daily_g,
        annual_co2_saved_kg=annual_kg,
        exposure_reduction_pct=calculate_exposure_reduction_pct(),
        calculation_basis=basis,
    )
