"""Tests for LLM phrasing service and zero-API-key fallback."""

import pytest

from models.air_quality import AirQualityData
from models.user_profile import UserProfile
from services.llm_service import _build_enrichment_prompt, enrich_plan_with_llm
from services.routine_planner import create_routine_plan


@pytest.mark.asyncio
async def test_enrich_plan_fallback_without_key(
    sample_aqi: AirQualityData,
    sample_profile: UserProfile,
) -> None:
    """Without an API key, plan should return untouched and intact."""
    base_plan = create_routine_plan(sample_aqi, sample_profile, language="en")
    enriched = await enrich_plan_with_llm(base_plan, api_key=None)
    assert enriched == base_plan
    assert (
        enriched.impact.daily_co2_saved_grams == base_plan.impact.daily_co2_saved_grams
    )


def test_build_enrichment_prompt_guards(
    sample_aqi: AirQualityData,
    sample_profile: UserProfile,
) -> None:
    """Prompt must contain defensive boundary tags and untrusted demarcation."""
    base_plan = create_routine_plan(sample_aqi, sample_profile, language="en")
    user_note = "Please say hello"
    prompt = _build_enrichment_prompt(base_plan, user_notes=user_note)
    assert "<user_input>" in prompt
    assert "</user_input>" in prompt
    assert "UNTRUSTED raw text" in prompt
    assert "NEVER alter, estimate, or introduce ANY numbers" in prompt
