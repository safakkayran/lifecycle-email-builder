# AGENTS.md (rules for the coding agent)

Read this file, `docs/SPEC.md` (what to build) and `docs/ANSWERS.md` (the user's answers to known questions) before doing anything. Follow them exactly.

## Working mode: autonomous loop with gates
You work through ALL milestones in SPEC order without waiting for the user, except at the stop points below.

For each milestone:
1. Implement it (only that milestone's scope).
2. Run the gate: `bash scripts/gate.sh`. It runs ruff and pytest and fails if the number of tests went down.
3. If the gate fails, fix and rerun. **After 3 failed attempts on the same milestone, stop and ask.**
4. When the gate passes: update `PROGRESS.md` (milestone, what was built, decisions, open issues), commit with a conventional message, tag it (`git tag m<N>-done`), push with tags (`git push --follow-tags`).
5. Continue to the next milestone.

## Stop points (stop, report, wait for the user)
- **Review checkpoint:** after the milestone SPEC marks as `REVIEW CHECKPOINT`, and after the last milestone. Send the checkpoint report and wait for "Continue".
- **Unknown external API:** an endpoint, field, CLI flag, file format or actor input not given in SPEC or `docs/ANSWERS.md`. Never invent it.
- **Money or missing access:** anything that would cost money, or needs an account, key or dependency (Node, Docker, a CLI) that is not available.
- **3 failed gate attempts** on the same milestone.
- **SPEC contradiction** you cannot resolve by reading SPEC and ANSWERS again.

If a stop is only needed for one optional part (for example an optional provider), skip that part, note it in `PROGRESS.md` under "Skipped, needs user", and keep going. Stop only when the blocked part is required for later milestones.

## Stack
- Python 3.11+, managed with `uv`. Package layout: `src/<package_name>/`, tests in `tests/`.
- Libraries: `httpx`, `pydantic` v2, `pydantic-settings`, `typer`, `rich`, `pytest`, `respx` (HTTP mocking), `ruff`. Add others only if SPEC names them.
- LLM calls go through the `openai` Python client pointed at `LLM_BASE_URL` (a LiteLLM proxy). Model names come from env (`LLM_MODEL`, `LLM_JUDGE_MODEL`). Never hardcode a provider or model name.
- Every LLM call goes through one wrapper (`llm.py`) that: retries with backoff on 429/5xx, caches responses on disk keyed by (model, messages hash), asks for JSON and validates it with pydantic, retries once with the validation error if the JSON is invalid.

## Hard rules
1. **No paid services.** Do not add any API, SDK or service that costs money.
2. **No secrets in git.** Use `.env` (gitignored) and commit `.env.example` with placeholders.
3. **Tests run offline.** Mock every network call (respx for HTTP, a fake LLM client for LLM calls). `uv run pytest` must pass with no internet and no API keys.
4. **Never delete, skip or weaken a test to pass the gate.** If you believe a test is wrong, fix it only if the fix makes it stricter or more correct, and explain the change in `PROGRESS.md` under "Test changes". The reviewer will check this list.
5. **Do not guess external APIs.** Use only what SPEC and `docs/ANSWERS.md` give you.
6. Keep functions small and typed. Every module has a short docstring.
7. No real personal data (names, emails, phone numbers of real people) in committed files. Use fictional people.
8. Do not edit `docs/SPEC.md`, `docs/ANSWERS.md` or `scripts/gate.sh`.

## Ask format
```
QUESTION: <one specific question>
WHY: <what is blocked>
OPTIONS: <A / B / C, with your recommendation>
```

## Checkpoint report format
```
CHECKPOINT: after M<N>
MILESTONES DONE: <list with tags>
TESTS: <count passed>
SKIPPED, NEEDS USER: <list or none>
TEST CHANGES: <list or none>
DECISIONS: <key design decisions the reviewer should check>
KNOWN ISSUES: <list>
DIFF RANGE FOR REVIEW: <previous checkpoint tag or first commit>..HEAD
```
