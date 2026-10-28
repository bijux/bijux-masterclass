#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
node "$ROOT/dist/src/main.js" inspect "$ROOT/fixtures/events.ndjson"
node "$ROOT/dist/src/main.js" filter "$ROOT/fixtures/events.ndjson" "$TMP/sales.ndjson" --kind sale
cat "$TMP/sales.ndjson"
node "$ROOT/dist/src/main.js" normalize "$ROOT/fixtures/events.ndjson" "$TMP/events.ndjson.gz" --gzip-output
node "$ROOT/dist/src/main.js" through "$ROOT/fixtures/events.ndjson" "$TMP/copy.ndjson" -- "$(command -v node)" -e 'process.stdin.pipe(process.stdout)'
