"""Tests for deterministic emission and exposure formulas (Requirement R6)."""

import pytest

from services.impact_engine import (
    build_impact_summary,
    calculate_commute_co2_savings,
    calculate_exposure_reduction_pct,
)


@pytest.mark.parametrize(
    "current_mode,alt_mode,dist_km,expected_daily_g",
    [
        ("car", "metro", 10.0, 2640.0),  # (140 - 8) * 20 = 2640
        ("motorcycle", "bus", 15.0, 720.0),  # (42 - 18) * 30 = 720
        ("car", "walk", 5.0, 1400.0),  # (140 - 0) * 10 = 1400
        ("walk", "car", 10.0, 0.0),  # No negative savings
        ("metro", "metro", 10.0, 0.0),  # Identical mode
    ],
)
def test_commute_co2_savings(
    current_mode: str,
    alt_mode: str,
    dist_km: float,
    expected_daily_g: float,
) -> None:
    """Verify commute carbon reduction calculation matches ARAI formulas."""
    result = calculate_commute_co2_savings(current_mode, alt_mode, dist_km)
    assert result == expected_daily_g


def test_exposure_reduction_all_measures() -> None:
    """Verify combined air cleaning measures yield bounded reduction."""
    reduction = calculate_exposure_reduction_pct(
        use_vent_timing=True,
        use_purifier_or_filter=True,
        use_cooking_exhaust=True,
        use_wet_cleaning=True,
    )
    # Multiplier: 0.70 * 0.25 * 0.40 * 0.65 = 0.0455 -> (1 - 0.0455) = 95.45% -> capped at 95.0%
    assert reduction == 95.0


def test_exposure_reduction_partial_measures() -> None:
    """Verify individual or partial filtration measures."""
    vent_only = calculate_exposure_reduction_pct(
        use_vent_timing=True,
        use_purifier_or_filter=False,
        use_cooking_exhaust=False,
        use_wet_cleaning=False,
    )
    assert vent_only == 30.0


def test_build_impact_summary() -> None:
    """Verify full impact summary structure and annual math."""
    summary = build_impact_summary("car", "metro", 10.0, working_days_per_year=250)
    assert summary.daily_co2_saved_grams == 2640.0
    assert summary.annual_co2_saved_kg == 660.0  # 2640 * 250 / 1000 = 660.0
    assert "ARAI baseline" in summary.calculation_basis
    assert summary.exposure_reduction_pct > 0.0
