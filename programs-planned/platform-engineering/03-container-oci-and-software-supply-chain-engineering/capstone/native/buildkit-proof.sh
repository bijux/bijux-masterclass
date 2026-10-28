#!/usr/bin/env sh
set -eu
command -v docker >/dev/null 2>&1 || { echo 'docker/buildx missing: not-executed' >&2; exit 2; }
OUT=${1:-"$(pwd)/native-evidence"}
mkdir -p "$OUT"
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
docker buildx version >"$OUT/buildx-version.txt"
for target in api worker probe; do
  docker buildx build \
    --file "$ROOT/workload/Containerfile.$target" \
    --platform linux/amd64,linux/arm64 \
    --provenance=mode=max \
    --sbom=true \
    --output "type=oci,dest=$OUT/atlas-$target.oci.tar" \
    "$ROOT/workload"
done
sha256sum "$OUT"/*.oci.tar >"$OUT/oci-archives.sha256"
echo "native BuildKit evidence written to $OUT"
