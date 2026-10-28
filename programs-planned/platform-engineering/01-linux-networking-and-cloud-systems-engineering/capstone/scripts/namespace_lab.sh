#!/bin/bash
set -euo pipefail

if [[ ${ALLOW_PRIVILEGED_LAB:-0} != 1 ]]; then
  echo "Set ALLOW_PRIVILEGED_LAB=1 inside a disposable Linux VM." >&2
  exit 2
fi
if [[ $EUID -ne 0 ]]; then
  echo "This network-namespace lab requires root in a disposable VM." >&2
  exit 2
fi
if ! python3 - <<'PY'
from pathlib import Path
value = 0
for line in Path('/proc/self/status').read_text().splitlines():
    if line.startswith('CapEff:'):
        value = int(line.split()[1], 16)
required = (1 << 12) | (1 << 21)  # CAP_NET_ADMIN and CAP_SYS_ADMIN
raise SystemExit(0 if value & required == required else 1)
PY
then
  echo "The environment lacks CAP_NET_ADMIN and CAP_SYS_ADMIN; use a disposable privileged VM." >&2
  exit 2
fi

left=atlas-left
right=atlas-right
cleanup() {
  ip netns del "$left" 2>/dev/null || true
  ip netns del "$right" 2>/dev/null || true
}
trap cleanup EXIT
cleanup
ip netns add "$left"
ip netns add "$right"
ip link add veth-left type veth peer name veth-right
ip link set veth-left netns "$left"
ip link set veth-right netns "$right"
ip -n "$left" addr add 192.0.2.1/30 dev veth-left
ip -n "$right" addr add 192.0.2.2/30 dev veth-right
ip -n "$left" link set lo up
ip -n "$right" link set lo up
ip -n "$left" link set veth-left up
ip -n "$right" link set veth-right up
ip netns exec "$left" ping -c 1 -W 1 192.0.2.2
ip -n "$left" route show
ip -n "$right" route show
