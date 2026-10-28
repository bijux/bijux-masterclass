#!/usr/bin/env sh
set -eu
cargo run --quiet --manifest-path "$(dirname "$0")/../Cargo.toml" -- demo
