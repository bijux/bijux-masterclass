#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
cargo run --quiet -- script scripts/demo.memory-workspace
