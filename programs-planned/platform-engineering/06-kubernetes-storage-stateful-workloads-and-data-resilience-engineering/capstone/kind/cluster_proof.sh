#!/usr/bin/env bash
set -euo pipefail

if [[ "${ALLOW_KIND_STORAGE_LAB:-0}" != "1" ]]; then
  echo "refusing to create a cluster: set ALLOW_KIND_STORAGE_LAB=1" >&2
  exit 2
fi
for tool in kind kubectl docker; do
  command -v "$tool" >/dev/null || {
    echo "required tool missing: $tool" >&2
    exit 3
  }
done

echo "The native lane requires a deliberately selected CSI and snapshot stack."
echo "Follow capstone/kind/README.md; no provider is installed implicitly."
