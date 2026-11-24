You are building `lifecycle-email-builder`, a portfolio repo for a GTM engineer. Work in this repository.

Read `AGENTS.md` (your rules and the autonomous loop), `docs/SPEC.md` (what to build) and `docs/ANSWERS.md` (the user's answers). Then:

1. Check the environment: `python3 --version`, `uv --version`, `node --version`, `git remote -v`. If something required is missing, stop and ask.
2. Read SPEC and ANSWERS once fully. If a REQUIRED answer is missing or contradicts SPEC, ask all such questions now in one message (QUESTION format), before writing code. Optional gaps: skip that part later and note it.
3. Start with M0, including `git submodule add https://github.com/coreyhaines31/marketingskills vendor/marketingskills`. Read its `skills/emails/SKILL.md`, `skills/product-marketing/SKILL.md` and `.claude-plugin/` and summarize their structure in `PROGRESS.md`. `scripts/gate.sh` already exists; make it executable and keep `.gate/` committed.
4. Run the loop from AGENTS.md: implement each milestone, pass `bash scripts/gate.sh`, update `PROGRESS.md`, commit, tag `m<N>-done`, push with tags, continue.
5. Stop only at the stop points in AGENTS.md. The first review checkpoint is after M4. Send the checkpoint report there and wait for "Continue".

Most important: no paid services, tests fully offline, never invent an external API, never weaken tests.
