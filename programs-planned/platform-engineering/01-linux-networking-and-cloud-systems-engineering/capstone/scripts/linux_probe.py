from __future__ import annotations

import json
import os
import platform
import resource
import socket
from pathlib import Path


def main() -> int:
    if not Path("/proc/self/status").exists():
        raise SystemExit("Linux /proc is required")
    status = {}
    for line in Path("/proc/self/status").read_text().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if key in {"Name", "Pid", "PPid", "Uid", "Gid", "FDSize", "VmRSS", "Threads", "CapEff", "NoNewPrivs"}:
                status[key] = value.strip()
    report = {
        "kernel": platform.release(),
        "status": status,
        "openFileLimit": resource.getrlimit(resource.RLIMIT_NOFILE),
        "cgroupV2": Path("/sys/fs/cgroup/cgroup.controllers").exists(),
        "addresses": sorted({item[4][0] for item in socket.getaddrinfo(socket.gethostname(), None)}),
        "effectiveUid": os.geteuid(),
    }
    cap = Path(__file__).resolve().parents[1]
    (cap / "reports" / "linux-probe.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
