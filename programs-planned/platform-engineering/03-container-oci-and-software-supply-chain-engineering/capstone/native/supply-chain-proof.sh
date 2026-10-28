#!/usr/bin/env sh
set -eu
: "${ATLAS_IMAGE:?set ATLAS_IMAGE to repository@sha256:digest}"
OUT=${1:-"$(pwd)/native-supply-chain-evidence"}
mkdir -p "$OUT"
for tool in syft grype cosign; do
  command -v "$tool" >/dev/null 2>&1 || { echo "$tool missing: not-executed" >&2; exit 2; }
done
syft version >"$OUT/syft-version.txt"
grype version >"$OUT/grype-version.txt"
cosign version >"$OUT/cosign-version.txt" 2>&1 || true
syft "$ATLAS_IMAGE" -o cyclonedx-json="$OUT/sbom.cdx.json"
grype "sbom:$OUT/sbom.cdx.json" -o json >"$OUT/vulnerabilities.json" || true
cosign verify-attestation --type slsaprovenance "$ATLAS_IMAGE" >"$OUT/provenance-verification.jsonl"
cosign tree "$ATLAS_IMAGE" >"$OUT/referrer-tree.txt"
echo 'Independent supply-chain evidence captured; apply the course verifier policy before authorizing release.'
