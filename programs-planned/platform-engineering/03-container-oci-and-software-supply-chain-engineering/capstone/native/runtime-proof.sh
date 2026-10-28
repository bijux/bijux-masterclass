#!/usr/bin/env sh
set -eu
RUNTIME=${OCI_RUNTIME:-runc}
command -v "$RUNTIME" >/dev/null 2>&1 || { echo "$RUNTIME missing: not-executed" >&2; exit 2; }
[ "$#" -eq 2 ] || { echo "usage: $0 BUNDLE_DIR EVIDENCE_DIR" >&2; exit 64; }
BUNDLE=$1
OUT=$2
ID="atlas-native-$$"
mkdir -p "$OUT"
cleanup() { "$RUNTIME" delete -f "$ID" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM
"$RUNTIME" --version >"$OUT/runtime-version.txt"
"$RUNTIME" spec --bundle "$BUNDLE" >/dev/null 2>&1 || true
"$RUNTIME" create --bundle "$BUNDLE" "$ID"
"$RUNTIME" state "$ID" >"$OUT/state-created.json"
"$RUNTIME" start "$ID"
"$RUNTIME" state "$ID" >"$OUT/state-started.json"
"$RUNTIME" kill "$ID" TERM
"$RUNTIME" delete "$ID"
trap - EXIT INT TERM
printf '%s\n' 'Native runtime lifecycle completed; inspect effective process/mount/cgroup evidence before claiming profile conformance.'
