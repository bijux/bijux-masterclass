#!/bin/sh
set -eu

ROOT=$(mktemp -d "${TMPDIR:-/tmp}/studyledger-demo.XXXXXX")
trap 'rm -rf "$ROOT"' EXIT HUP INT TERM
export STUDY_LEDGER_FILE="$ROOT/ledger.json"
MAIN="$(dirname "$0")/../dist/src/main.js"

node "$MAIN" plan --topic "JavaScript runtime values" --minutes 30
node "$MAIN" plan --topic "TypeScript narrowing" --minutes 45
node "$MAIN" start 1
node "$MAIN" complete 1 --minutes 28 --note "Rebuilt the examples without notes"
node "$MAIN" abandon 2 --reason "Moved to next week"
node "$MAIN" list
node "$MAIN" summary
