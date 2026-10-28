#!/bin/bash
set -euo pipefail

if [[ ${ALLOW_RESOURCE_LAB:-0} != 1 ]]; then
  echo "Set ALLOW_RESOURCE_LAB=1 inside a disposable Linux VM." >&2
  exit 2
fi

systemd-run --user --wait --collect   --property=MemoryMax=96M   --property=CPUQuota=50%   python3 -c 'x=[]; import time; [x.append(bytearray(1024*1024)) for _ in range(64)]; time.sleep(1)'
