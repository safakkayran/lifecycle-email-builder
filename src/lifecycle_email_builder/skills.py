"""Skill loader for marketingskills submodule."""

from __future__ import annotations

from lifecycle_email_builder.config import get_settings


def load_skill_markdown(skill_name: str, max_chars: int | None = None) -> str | None:
    """Load a skill's SKILL.md body (without frontmatter), truncated to max_chars."""
    settings = get_settings()
    skill_path = settings.VENDOR_DIR / "skills" / skill_name / "SKILL.md"

    if not skill_path.exists():
        return None

    content = skill_path.read_text(encoding="utf-8")

    # Strip frontmatter (between --- lines)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    if max_chars and len(content) > max_chars:
        content = content[:max_chars] + "\n\n[TRUNCATED]"

    return content


def load_relevant_skills(step: str) -> dict[str, str]:
    """Load skill context relevant to a pipeline step."""
    skill_map = {
        "context": ["product-marketing"],
        "voice": ["copywriting", "product-marketing"],
        "funnel": ["emails", "onboarding", "churn-prevention", "paywalls"],
        "draft": ["emails", "copywriting", "copy-editing"],
        "lint": ["copy-editing", "copywriting"],
    }

    skills = skill_map.get(step, [])
    results = {}

    for skill in skills:
        content = load_skill_markdown(skill, get_settings().SKILL_CONTEXT_MAX_CHARS)
        if content:
            results[skill] = content

    return results