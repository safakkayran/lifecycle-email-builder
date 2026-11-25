"""Pydantic models for lifecycle-email-builder."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class FunnelStage(StrEnum):
    WELCOME = "welcome"
    ACTIVATION = "activation"
    NURTURE = "nurture"
    TRIAL_END = "trial_end"
    UPSELL = "upsell"
    WINBACK = "winback"


ALL_STAGES = list(FunnelStage)


class BlockType(StrEnum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    BULLET_LIST = "bullet_list"
    QUOTE = "quote"


class Block(BaseModel):
    type: BlockType
    content: str | list[str]  # string for heading/paragraph/quote, list for bullet_list
    level: int | None = None  # for heading: 1-3


class FunnelStageConfig(BaseModel):
    id: FunnelStage
    name: str
    goal: str


class EmailSpec(BaseModel):
    id: str
    stage: FunnelStage
    trigger_event: str
    delay_hours: int = Field(ge=0)
    goal: str
    exit_condition: str
    subject_angle: str


class EmailDraft(BaseModel):
    id: str
    subject: str
    preview_text: str
    blocks: list[Block]
    cta_text: str
    cta_url_placeholder: str = "{{cta_url}}"


class FunnelMap(BaseModel):
    stages: list[FunnelStageConfig]
    emails: list[EmailSpec]

    def validate_structure(self) -> list[str]:
        """Validate funnel structure. Returns list of errors."""
        errors = []

        # Check all 6 stages present
        stage_ids = {e.stage for e in self.emails}
        for stage in ALL_STAGES:
            if stage not in stage_ids:
                errors.append(f"Missing stage: {stage.value}")

        # Check email count 12-16
        count = len(self.emails)
        if count < 12:
            errors.append(f"Too few emails: {count} (minimum 12)")
        if count > 16:
            errors.append(f"Too many emails: {count} (maximum 16)")

        # Check delays non-negative
        for email in self.emails:
            if email.delay_hours < 0:
                errors.append(f"Negative delay for {email.id}: {email.delay_hours}")

        return errors


class ProductContext(BaseModel):
    """Product marketing context from step 1."""
    product_overview: str
    target_audience: str
    personas: list[str] = Field(default_factory=list)
    problems_pain_points: str
    competitive_landscape: str
    differentiation: str
    objections: list[str] = Field(default_factory=list)
    switching_dynamics: str
    customer_language: list[str] = Field(default_factory=list)
    brand_voice: str
    proof_points: list[str] = Field(default_factory=list)
    goals: str


class VoiceGuide(BaseModel):
    """Brand voice guide from step 2."""
    attributes: list[dict[str, str]]
    tone_by_context: dict[str, str]
    terms_we_own: list[str]
    never_use: list[str]


class LintResult(BaseModel):
    email_id: str
    passed: bool
    rules: dict[str, bool]
    errors: list[str]


class RenderResult(BaseModel):
    email_id: str
    mjml_path: str
    html_path: str
    success: bool
    error: str | None = None


class ExportItem(BaseModel):
    id: str
    stage: str
    trigger_event: str
    delay_hours: int
    subject: str
    preview: str
    html_path: str


class RunResult(BaseModel):
    product_context_path: str
    voice_path: str | None
    funnel_path: str
    emails_dir: str
    mjml_dir: str
    html_dir: str
    export_dir: str
    gallery_path: str
    lint_results: list[LintResult]
    render_results: list[RenderResult]