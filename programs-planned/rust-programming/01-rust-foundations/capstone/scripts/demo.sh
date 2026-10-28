#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
storage=$(mktemp "${TMPDIR:-/tmp}/taskboard-demo.XXXXXX")
rm -f "$storage"
trap 'rm -f "$storage"' EXIT

export TASKBOARD_FILE="$storage"
cd "$root"

cargo run --quiet -- add high "Repair record parser"
cargo run --quiet -- add normal "Write storage tests"
cargo run --quiet -- rename 2 "Write persistence and CLI tests"
cargo run --quiet -- start 1
cargo run --quiet -- done 1
cargo run --quiet -- list
cargo run --quiet -- search parser
cargo run --quiet -- stats

expected_header='TASKBOARD-V1'
actual_header=$(head -n 1 "$storage")
[[ "$actual_header" == "$expected_header" ]]
