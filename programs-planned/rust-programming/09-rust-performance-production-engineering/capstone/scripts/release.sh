#!/usr/bin/env bash
set -euo pipefail

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

revision=${METRICRAIL_SOURCE_REVISION:-unknown}
profile=${METRICRAIL_PROFILE:-dist}
export METRICRAIL_SOURCE_REVISION=$revision
export METRICRAIL_PROFILE=$profile

if [[ ! -f Cargo.lock ]]; then
    cargo generate-lockfile
fi
cargo build --locked --profile "$profile"
artifact="target/$profile/metricrail"
if [[ ! -f "$artifact" ]]; then
    printf 'missing release artifact: %s\n' "$artifact" >&2
    exit 1
fi

if command -v sha256sum >/dev/null 2>&1; then
    digest=$(sha256sum "$artifact" | awk '{print $1}')
elif command -v shasum >/dev/null 2>&1; then
    digest=$(shasum -a 256 "$artifact" | awk '{print $1}')
else
    printf 'no SHA-256 utility available\n' >&2
    exit 1
fi

bytes=$(wc -c < "$artifact" | tr -d ' ')
target=$($artifact version | awk -F= '$1 == "target" { print $2 }')
{
    printf 'artifact=metricrail\n'
    printf 'bytes=%s\n' "$bytes"
    printf 'profile=%s\n' "$profile"
    printf 'sha256=%s\n' "$digest"
    printf 'source_revision=%s\n' "$revision"
    printf 'target=%s\n' "$target"
} | LC_ALL=C sort
