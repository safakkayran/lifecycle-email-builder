# lifecycle-email-builder Progress Log

## M0 - Scaffold ✅
- `uv init --package lifecycle-email-builder` with src layout (`src/lifecycle_email_builder/`)
- Dependencies: pydantic, pydantic-settings, typer, rich, httpx, selectolax, python-dotenv, pyyaml, jinja2, openai, tenacity
- Dev deps: pytest, pytest-asyncio, respx, ruff
- GitHub Actions CI, `.env.example`, trivial import test
- **Submodule added**: `vendor/marketingskills` (coreyhaines31/marketingskills)
- **Skill loader** (`skills.py`): loads SKILL.md bodies, strips frontmatter, truncates to 12000 chars
- **Relevant skills per step**:
  - `context`: product-marketing
  - `voice`: copywriting, product-marketing
  - `funnel`: emails, onboarding, churn-prevention, paywalls
  - `draft`: emails, copywriting, copy-editing
  - `lint`: copy-editing, copywriting
- **Submodule structure** (from `vendor/marketingskills/skills/`):
  - `emails/SKILL.md`: Email sequence design (welcome, nurture, re-engagement, onboarding). References: sequence-templates.md, email-types.md, copy-guidelines.md
  - `product-marketing/SKILL.md`: Product marketing context doc (14 sections). Output format: `.agents/product-marketing.md` with version/changelog/learnings
  - `.claude-plugin/`: Contains `plugin.json` (name, description, version, author, homepage, repository, license, skills path) and `marketplace.json` (name, owner, metadata, plugins array)
- Gate: PASSED (9 tests)
- Tag: `m0-done`

---

## M1 - LLM wrapper + skill loader
- Status: NOT STARTED

---

## M2 - Fetch + step 1 product context + step 2 voice
- Status: NOT STARTED

---

## M3 - Step 3 funnel map
- Status: NOT STARTED

---

## M4 - Step 4 drafts + step 5 lint/fix (REVIEW CHECKPOINT)
- Status: NOT STARTED

---

## M5 - Step 6 render (Jinja2 → MJML → HTML) + gallery
- Status: NOT STARTED

---

## M6 - Step 7 exports
- Status: NOT STARTED

---

## M7 - Claude Code plugin folder
- Status: NOT STARTED

---

## M8 - Examples + polish (FINAL REVIEW CHECKPOINT)
- Status: NOT STARTED

---

## Decisions
- Package name: `lifecycle-email-builder` (distribution), module: `lifecycle_email_builder`
- Python 3.11+
- LiteLLM models: nim-laguna (worker), nim-step (judge)
- Node v26.12.1 available for MJML
- Loops export: SKIP (generic.json only)
- Customer.io export: SKIP (generic.json only)
- Example products: https://attio.com, https://cal.com
- Brand defaults: neutral (grayscale)

## Skipped, needs user
- None yet