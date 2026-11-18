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
    # Multiplicative survival model: (1 - E_total) = Product(1 - E_i)
    multiplier = 1.0
    if use_vent_timing:
        multiplier *= 1.0 - VENT_TIMING_REDUCTION
    if use_purifier_or_filter:
        multiplier *= 1.0 - HEPA_PURIFIER_REDUCTION
    if use_cooking_exhaust:
        multiplier *= 1.0 - COOKING_VENT_REDUCTION
    if use_wet_cleaning:
        multiplier *= 1.0 - WET_CLEANING_REDUCTION

    reduction_pct = (1.0 - multiplier) * 100.0
    return min(95.0, round(reduction_pct, 1))


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
    reduction_pct = calculate_exposure_reduction_pct()

    basis = (
        f"CO2 savings calculated using ARAI baseline: "
        f"{current_mode} ({get_emission_factor(current_mode)}g/km) vs "
        f"{alternative_mode} ({get_emission_factor(alternative_mode)}g/km) "
        f"over {commute_distance_km * 2:.1f} km roundtrip."
    )

    return ImpactSummary(
        daily_co2_saved_grams=daily_g,
        annual_co2_saved_kg=annual_kg,
        exposure_reduction_pct=reduction_pct,
        calculation_basis=basis,
    )
