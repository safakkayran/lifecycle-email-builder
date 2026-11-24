#!/usr/bin/env bash
# Milestone gate: lint + tests + "test count must not go down".
# Copy to scripts/gate.sh in each repo. The agent must not edit this file.
set -uo pipefail

STATE_DIR=".gate"
COUNT_FILE="$STATE_DIR/test_count"
mkdir -p "$STATE_DIR"

echo "== ruff =="
if ! uv run ruff check .; then
  echo "GATE FAIL: ruff"
  exit 1
fi

echo "== pytest =="
OUT=$(uv run pytest -q 2>&1)
STATUS=$?
echo "$OUT" | tail -n 15
if [ $STATUS -ne 0 ]; then
  echo "GATE FAIL: tests"
  exit 1
fi

PASSED=$(echo "$OUT" | grep -Eo '[0-9]+ passed' | tail -n1 | grep -Eo '[0-9]+' || echo 0)
PREV=$(cat "$COUNT_FILE" 2>/dev/null || echo 0)

if [ "$PASSED" -lt "$PREV" ]; then
  echo "GATE FAIL: test count went down ($PREV -> $PASSED). Tests must not be removed."
  exit 1
fi

echo "$PASSED" > "$COUNT_FILE"
echo "GATE PASS: $PASSED tests (previous $PREV)"
