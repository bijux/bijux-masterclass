#!/usr/bin/env bash
set -euo pipefail
manifest="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/Cargo.toml"
set +e
output="$(cargo run --quiet --manifest-path "$manifest" -- demo)"
status=$?
set -e
if [[ $status -ne 1 ]]; then
  printf 'expected demo exit 1, got %s\n' "$status" >&2
  exit 1
fi
grep -q 'accepted: false' <<<"$output"
grep -q 'S-002' <<<"$output"
printf '%s\n' "$output"
