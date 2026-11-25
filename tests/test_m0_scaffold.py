"""M0 scaffold tests."""

from __future__ import annotations

from lifecycle_email_builder import __version__
from lifecycle_email_builder.config import get_settings
from lifecycle_email_builder.models import EmailSpec, FunnelMap, FunnelStage
from lifecycle_email_builder.skills import load_relevant_skills, load_skill_markdown


def test_version():
    """Version is set."""
    assert __version__ == "0.1.0"


def test_settings_load():
    """Settings load without error."""
    settings = get_settings()
    assert settings.LLM_MODEL == "nim-laguna"
    assert settings.LLM_JUDGE_MODEL == "nim-step"
    assert settings.LITELLM_BASE_URL == "http://127.0.0.1:4000"


def test_funnel_map_validation():
    """FunnelMap validates structure."""
    funnel = FunnelMap(
        stages=[],
        emails=[
            EmailSpec(
                id=f"email_{i}",
                stage=FunnelStage.WELCOME,
                trigger_event="signup",
                delay_hours=i * 24,
                goal="test",
                exit_condition="purchase",
                subject_angle="test",
            )
            for i in range(12)
        ],
    )

    errors = funnel.validate_structure()
    # Should have errors for missing stages
    assert len(errors) == 5  # 5 other stages missing
    assert any("activation" in e for e in errors)
    assert any("nurture" in e for e in errors)
    assert any("trial_end" in e for e in errors)
    assert any("upsell" in e for e in errors)
    assert any("winback" in e for e in errors)


def test_funnel_map_valid():
    """FunnelMap with all stages passes."""
    funnel = FunnelMap(
        stages=[],
        emails=[
            EmailSpec(
                id=f"email_{i}",
                stage=stage,
                trigger_event="signup",
                delay_hours=i * 24,
                goal="test",
                exit_condition="purchase",
                subject_angle="test",
            )
            for i, stage in enumerate(FunnelStage)
            for _ in range(2)  # 2 emails per stage = 12 total
        ],
    )

    errors = funnel.validate_structure()
    assert errors == []


def test_load_emails_skill():
    """Load emails skill from submodule."""
    content = load_skill_markdown("emails")
    assert content is not None
    assert "Email Sequence Design" in content
    assert "Welcome Sequence" in content


def test_load_product_marketing_skill():
    """Load product-marketing skill from submodule."""
    content = load_skill_markdown("product-marketing")
    assert content is not None
    assert "Product Marketing Context" in content
    assert "Document version" in content


def test_load_relevant_skills_context():
    """Load skills for context step."""
    skills = load_relevant_skills("context")
    assert "product-marketing" in skills
    assert len(skills) == 1


def test_load_relevant_skills_funnel():
    """Load skills for funnel step."""
    skills = load_relevant_skills("funnel")
    expected = {"emails", "onboarding", "churn-prevention", "paywalls"}
    assert set(skills.keys()) == expected


def test_load_relevant_skills_unknown():
    """Unknown step returns empty."""
    skills = load_relevant_skills("unknown")
    assert skills == {}