#!/bin/sh
set -eu

ROOT="${TMPDIR:-/tmp}/framevault-demo-$$"
ARCHIVE="$ROOT/demo.fv"
OUT="$ROOT/out"
mkdir -p "$ROOT/source"
printf 'binary\000payload\n' > "$ROOT/source/payload.bin"
printf 'systems course\n' > "$ROOT/source/notes.txt"

cargo run --quiet --manifest-path "$(dirname "$0")/../Cargo.toml" -- \
    create "$ARCHIVE" \
    --entry "data/payload.bin" "$ROOT/source/payload.bin" \
    --entry "docs/notes.txt" "$ROOT/source/notes.txt"
cargo run --quiet --manifest-path "$(dirname "$0")/../Cargo.toml" -- list "$ARCHIVE"
cargo run --quiet --manifest-path "$(dirname "$0")/../Cargo.toml" -- verify "$ARCHIVE"
cargo run --quiet --manifest-path "$(dirname "$0")/../Cargo.toml" -- extract "$ARCHIVE" "$OUT"
cmp "$ROOT/source/payload.bin" "$OUT/data/payload.bin"
cmp "$ROOT/source/notes.txt" "$OUT/docs/notes.txt"
rm -rf "$ROOT"
