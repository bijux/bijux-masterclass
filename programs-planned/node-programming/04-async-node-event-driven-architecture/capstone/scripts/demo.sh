#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
node "$ROOT/dist/src/main.js" inspect "$ROOT/fixtures/demo.json"
node "$ROOT/dist/src/main.js" run "$ROOT/fixtures/demo.json" --concurrency 2
node "$ROOT/dist/src/main.js" run "$ROOT/fixtures/failure.json" --policy continue || test $? -eq 1
