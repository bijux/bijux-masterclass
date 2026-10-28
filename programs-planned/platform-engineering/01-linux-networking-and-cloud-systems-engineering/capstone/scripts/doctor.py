from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import sys
from pathlib import Path

CAP_NET_ADMIN = 12
CAP_SYS_ADMIN = 21


def command(name: str) -> dict[str, object]:
    path = shutil.which(name)
    return {"available": path is not None, "path": path}


def effective_capabilities() -> int:
    if not sys.platform.startswith("linux"):
        return 0
    try:
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("CapEff:"):
                return int(line.split()[1], 16)
    except OSError:
        pass
    return 0


def has_capability(mask: int, number: int) -> bool:
    return bool(mask & (1 << number))


def main() -> int:
    linux = sys.platform.startswith("linux")
    cgroup_v2 = Path("/sys/fs/cgroup/cgroup.controllers").exists() if linux else False
    systemd_pid1 = False
    if linux:
        try:
            systemd_pid1 = Path("/proc/1/comm").read_text().strip() == "systemd"
        except OSError:
            pass
    cap_eff = effective_capabilities()
    net_admin = has_capability(cap_eff, CAP_NET_ADMIN)
    sys_admin = has_capability(cap_eff, CAP_SYS_ADMIN)
    root_uid = bool(linux and hasattr(os, "geteuid") and os.geteuid() == 0)

    report = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "effectiveUid": os.geteuid() if hasattr(os, "geteuid") else None,
        "linux": linux,
        "procAvailable": Path("/proc/self/status").exists(),
        "cgroupV2": cgroup_v2,
        "systemdPid1": systemd_pid1,
        "capabilities": {
            "effectiveHex": f"{cap_eff:016x}",
            "netAdmin": net_admin,
            "sysAdmin": sys_admin,
        },
        "commands": {name: command(name) for name in [
            "bash", "ip", "ss", "ps", "lsof", "strace", "openssl", "nft",
            "systemctl", "systemd-analyze", "dig", "curl", "tar", "mount", "unshare",
            "nginx", "cloud-init",
        ]},
        "evidenceClasses": {
            "A_dependencyLight": True,
            "B_localRuntime": linux and Path("/proc").exists(),
            "C_privilegedVm": root_uid and systemd_pid1 and net_admin and sys_admin,
            "D_realCloud": bool(os.environ.get("ATLAS_REAL_CLOUD_PROOF")),
        },
        "labCapabilities": {
            "systemdInstallation": systemd_pid1 and root_uid,
            "networkNamespacesAndFirewall": root_uid and net_admin and sys_admin,
            "mountAndBoot": root_uid and sys_admin,
            "cgroupResourceControl": cgroup_v2 and systemd_pid1,
        },
    }
    target = Path(__file__).resolve().parents[1] / "reports" / "doctor.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
