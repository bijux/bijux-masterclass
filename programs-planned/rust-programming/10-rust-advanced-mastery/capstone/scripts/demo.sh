#!/usr/bin/env sh
set -eu
root="${TMPDIR:-/tmp}/axiomstore-demo-$$"
archive="$root/demo.ax"
legacy="$root/legacy.txt"
mkdir -p "$root"
printf 'first=one\nsecond=two\n' > "$legacy"
cargo run --quiet -- init "$archive"
cargo run --quiet -- put "$archive" alpha one
cargo run --quiet -- put "$archive" beta two
cargo run --quiet -- list "$archive"
cargo run --quiet -- verify "$archive"
rm -f "$archive"
cargo run --quiet -- migrate-v0 "$legacy" "$archive"
cargo run --quiet -- list "$archive"
rm -rf "$root"
