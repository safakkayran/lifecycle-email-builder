# ANSWERS.md

Fill this in BEFORE starting the loop and save it as `docs/ANSWERS.md` in the repo.
Delete the sections for other repos. Write "SKIP" for anything you want the agent to leave out.
The agent may only use external API details written here or in SPEC.

## Common (all repos)
- GitHub repo URL: https://github.com/safakkayran/lifecycle-email-builder
- Git push works from the server (yes/no): yes (HTTPS via gh auth)
- `node --version` output (or "not installed"): v26.12.1
- LiteLLM base URL (e.g. http://localhost:4000): http://127.0.0.1:4000
- Model alias for generation (LLM_MODEL): nim-laguna
- Model alias for evals judge (LLM_JUDGE_MODEL, must differ): nim-step

---

## lifecycle-email-builder
- Node available for MJML (yes/no): yes (v26.12.1)
- Loops export: SKIP (only generic.json)
- Customer.io export: SKIP (only generic.json)
- Two example product URLs for the demo:
  - https://attio.com
  - https://cal.com
- Brand defaults for `brand.yaml` (primary color hex, font) or "neutral": neutral (default grayscale)