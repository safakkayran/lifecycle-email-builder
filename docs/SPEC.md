# lifecycle-email-builder: SPEC

**Pitch:** Point it at a product URL and get a complete lifecycle email program: product context, brand voice guide, a funnel map (signup, activation, nurture, trial end, upsell, win-back), and ready-to-render MJML templates with triggers and timing. Built on top of the open-source `coreyhaines31/marketingskills` library (MIT) and usable both as a CLI and as a Claude Code plugin.

Package name: `lifecycle_builder`. CLI name: `lifecycle`.

## How it uses marketingskills (important)
- Vendor it as a **git submodule** at `vendor/marketingskills` (pinned commit). Credit it in README and keep its LICENSE. Do not fork, do not copy its files into `src/`.
- At runtime, the pipeline **loads relevant `SKILL.md` files as reference context** for the LLM: `product-marketing` (context doc format), `emails` (sequence design), `onboarding`, `churn-prevention`, `paywalls` (upsell moments), `copywriting`, `copy-editing`. Load only the SKILL.md body, truncated to `SKILL_CONTEXT_MAX_CHARS` (default 12000) per call, because free models have smaller context windows.
- The agent must **read the actual files in the submodule** to learn their structure (frontmatter, sections). Do not assume.

## Pipeline
```
URL ──> fetch site text (homepage, pricing, about, features; Jina Reader or httpx)
   ──> step 1 product context  → out/<slug>/product-marketing.md   (format follows the vendored product-marketing skill)
   ──> step 2 voice guide      → out/<slug>/voice.md               (skipped if --voice-file given)
   ──> step 3 funnel map       → out/<slug>/funnel.yaml            (stages, emails, trigger event, delay, goal, exit condition)
   ──> step 4 email drafts     → out/<slug>/emails/<id>.json       (subject, preview, body blocks, CTA)
   ──> step 5 lint + fix       (rules below; one LLM fix pass for failures)
   ──> step 6 render           → out/<slug>/mjml/<id>.mjml and html/<id>.html
   ──> step 7 export           → out/<slug>/export/loops.json | customerio.json | generic.json
   ──> out/<slug>/index.html   (simple static gallery of all emails, grouped by stage)
```
Each step is a separate function and a separate CLI subcommand, reading the previous step's files, so a user can edit `funnel.yaml` by hand and re-run from step 4.

## Models (pydantic)
- `FunnelStage(id, name, goal)`; stages fixed: `welcome`, `activation`, `nurture`, `trial_end`, `upsell`, `winback`.
- `EmailSpec(id, stage, trigger_event, delay_hours, goal, exit_condition, subject_angle)`. Funnel target: 12 to 16 emails total.
- `EmailDraft(id, subject, preview_text, blocks: list[Block], cta_text, cta_url_placeholder)`; `Block` is `heading | paragraph | bullet_list | quote`.

## Lint rules (`lint.py`, pure Python)
Subject under 60 chars, preview under 110 chars, body under 180 words (welcome may be 250), exactly one primary CTA, no em dashes, no banned phrases (`rules/banned.txt`), placeholders only from an allowed set (`{{first_name}}`, `{{product_name}}`, `{{cta_url}}`), every email in `funnel.yaml` has a draft. Report pass/fail per rule; failures go to one LLM fix pass; still failing → reported, not hidden.

## Rendering
- MJML via the official `mjml` npm CLI (`npx mjml in.mjml -o out.html`). Requires Node 18+; the agent must check `node --version` and ask the user if missing. Fallback if Node is unavailable: write the `.mjml` only and say so.
- MJML generated from Jinja2 templates in `templates/` (one base layout + block partials). Colors and font from `brand.yaml` (user editable; defaults neutral).

## Exports
- `generic.json`: list of `{id, stage, trigger_event, delay_hours, subject, preview, html_path}`.
- `loops.json` and `customerio.json`: **the agent must not invent these platforms' import formats.** Implement them only if `docs/ANSWERS.md` contains the official format docs; otherwise ship only `generic.json` and a README note.

## Claude Code plugin
- Folder `plugin/` containing a plugin manifest and one skill `lifecycle-email-builder/SKILL.md` that tells Claude how to run the CLI and how to review the output.
- **Copy the manifest structure from the vendored marketingskills repo** (`vendor/marketingskills/.claude-plugin/`). Do not invent fields. If unclear, ask the user.

## CLI
- `lifecycle build <url> [--slug] [--voice-file voice.md] [--from-step N]`
- `lifecycle context <url>` / `voice` / `funnel` / `draft` / `lint` / `render` / `export` (single steps)
- `lifecycle doctor` (LLM reachable, Node present, submodule present)

## Examples
`examples/`: full output for 2 public products (choose well-known B2B SaaS with public marketing sites; only public info; brand names may appear in context files but the README must say these are unaffiliated demos). Commit `funnel.yaml`, emails JSON, HTML gallery screenshots (PNG) for the README.

## Milestones
- **M0 Scaffold** (uv, ruff, pytest, CI, `.env.example`, `PROGRESS.md`) + add the submodule and read its structure; report the SKILL.md format you found.
- **M1 LLM wrapper + skill loader** (`skills.py`: load, strip frontmatter, truncate). Tests on a fake skills folder.
- **M2 Fetch + step 1 product context + step 2 voice.** Tests with fixture HTML and fake LLM.
- **M3 Step 3 funnel map.** Validate 12 to 16 emails, all 6 stages present, delays non-negative. Tests.
- **M4 Step 4 drafts + step 5 lint/fix (REVIEW CHECKPOINT).** Tests for every lint rule.
- **M5 Step 6 render** (Jinja2 → MJML → HTML) + gallery `index.html`. Tests: MJML string structure; HTML render test skipped if Node missing.
- **M6 Step 7 exports** (generic first, others only if docs are in ANSWERS).
- **M7 Claude Code plugin folder.**
- **M8 Examples + polish (FINAL REVIEW CHECKPOINT):** two real runs, README (pitch, diagram, quickstart, screenshots, "built on marketingskills" credit, design decisions: step-by-step editable artifacts, lint-then-fix loop, free-model context budget), `demo.tape`.

## Done means
Offline tests green, CI green, `lifecycle build <url>` produces a full folder for a real product, gallery screenshots in README, plugin folder present.
