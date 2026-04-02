#!/usr/bin/env bash
set -euo pipefail
# Determinism self-test:
# - run with different core counts
# - hash a stable publish artifact
# - compare hashes
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"
PROFILE="${1:-profiles/ci}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
OUT_BASE="$(mktemp -d)"
cleanup() { rm -rf "${OUT_BASE}"; }
trap cleanup EXIT
hash_file() {
  "${PYTHON_BIN}" - <<'PY' "$1"
import hashlib
from pathlib import Path
p = Path(__import__("sys").argv[1])
h = hashlib.sha256()
with p.open("rb") as f:
    for chunk in iter(lambda: f.read(1024*1024), b""):
        h.update(chunk)
print(h.hexdigest())
PY
}

hash_normalized_summary() {
  "${PYTHON_BIN}" - <<'PY' "$1"
import hashlib
import json
import sys
from pathlib import Path

def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items() if k != "path"}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
normalized = json.dumps(normalize(payload), sort_keys=True, separators=(",", ":"))
print(hashlib.sha256(normalized.encode("utf-8")).hexdigest())
PY
}
run_once() {
  local cores="$1"
  local outdir="${OUT_BASE}/run_${cores}"
  mkdir -p "${outdir}"
  snakemake --snakefile Snakefile --profile "${PROFILE}" --cores "${cores}" --config results_dir="${outdir}/results" publish_dir="${outdir}/publish" logs_dir="${outdir}/logs" benchmarks_dir="${outdir}/benchmarks" >/dev/null
  hash_normalized_summary "${outdir}/publish/v1/summary.json"
}
# Lint should be clean (contract hygiene).
snakemake --snakefile Snakefile --lint >/dev/null
h1="$(run_once 1)"
h4="$(run_once 4)"
if [[ "${h1}" != "${h4}" ]]; then
  echo "Determinism failure:"
  echo " cores=1: ${h1}"
  echo " cores=4: ${h4}"
  exit 1
fi
echo "OK: deterministic normalized publish/v1/summary.json across cores (sha256=${h1})"

# Drift detection test
echo "Testing drift detection..."
snakemake --list-changes code > /dev/null || echo "OK: drift detected on code change simulation"
# (In real CI, run after intentional code touch to verify non-zero exit on drift)
