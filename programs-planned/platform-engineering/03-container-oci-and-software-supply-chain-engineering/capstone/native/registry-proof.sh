#!/usr/bin/env sh
set -eu
command -v oras >/dev/null 2>&1 || { echo 'oras missing: not-executed' >&2; exit 2; }
: "${ATLAS_REGISTRY:?set ATLAS_REGISTRY to an isolated registry host/repository prefix}"
: "${ATLAS_SUBJECT_DIGEST:?set ATLAS_SUBJECT_DIGEST to the approved sha256 digest}"
OUT=${1:-"$(pwd)/native-registry-evidence"}
mkdir -p "$OUT"
oras version >"$OUT/oras-version.txt"
oras manifest fetch "$ATLAS_REGISTRY/atlas-api@$ATLAS_SUBJECT_DIGEST" >"$OUT/manifest.json"
oras discover --format json "$ATLAS_REGISTRY/atlas-api@$ATLAS_SUBJECT_DIGEST" >"$OUT/referrers.json"
printf '%s  %s\n' "$ATLAS_SUBJECT_DIGEST" "$ATLAS_REGISTRY/atlas-api" >"$OUT/subject.txt"
echo 'Registry read/referrer evidence captured. Authentication, retention, replication, garbage collection, and recovery require separate controlled tests.'
