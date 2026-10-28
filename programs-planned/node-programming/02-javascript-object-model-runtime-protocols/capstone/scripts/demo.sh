#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="${TMPDIR:-/tmp}/objectatlas-demo-$$.json"
trap 'rm -f "$FILE"' EXIT
run() { OBJECT_ATLAS_FILE="$FILE" node "$ROOT/dist/src/main.js" "$@"; }
run add root folder "Root"
run add api service "API" --parent root
run set api port 8080
run add ui component "Web UI" --parent root
run walk --order breadth
run clone root copy
run summary
