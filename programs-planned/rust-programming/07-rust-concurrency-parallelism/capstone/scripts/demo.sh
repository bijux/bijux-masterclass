#!/usr/bin/env sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/.." && pwd)
cd "$ROOT"
cargo run --quiet -- inspect examples/demo.batchweave
cargo run --quiet -- run examples/demo.batchweave --workers 4 --queue-capacity 2 --report-threads 2
cargo run --quiet -- demo
