#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cargo run --manifest-path "$root/Cargo.toml" -- analyze "$root/fixtures/valid.tsv"
cargo run --manifest-path "$root/Cargo.toml" -- version
