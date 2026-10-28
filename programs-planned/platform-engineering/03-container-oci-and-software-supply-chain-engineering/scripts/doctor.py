#!/usr/bin/env python3
from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

COURSE = Path(__file__).resolve().parents[1]


def version(command: str, args: list[str] | None = None) -> dict[str, str]:
    path = shutil.which(command)
    if not path:
        return {"status": "missing"}
    try:
        result = subprocess.run([path, *(args or ["--version"])], capture_output=True, text=True, timeout=8)
        output = (result.stdout or result.stderr).strip().splitlines()
        first = output[0] if output else f"exit={result.returncode}"
    except Exception as exc:
        first = f"error: {exc}"
    return {"status": "present", "path": path, "version": first}


report = {
    "course": "03-container-oci-and-software-supply-chain-engineering",
    "host": {"platform": platform.platform(), "machine": platform.machine(), "uid": str(getattr(__import__('os'), 'getuid', lambda: -1)())},
    "mandatory": {
        "python": {"status": "present", "version": sys.version.split()[0], "ok": sys.version_info >= (3, 11)},
        "go": version("go", ["version"]),
        "openssl": version("openssl", ["version"]),
    },
    "independentLanes": {
        name: version(name) for name in [
            "docker", "podman", "buildctl", "runc", "crun", "oras", "skopeo",
            "cosign", "syft", "grype", "mkdocs",
        ]
    },
    "kernel": {},
}
for name, path in {
    "unprivilegedUserNamespaces": "/proc/sys/kernel/unprivileged_userns_clone",
    "userMaxUserNamespaces": "/proc/sys/user/max_user_namespaces",
    "cgroupControllers": "/sys/fs/cgroup/cgroup.controllers",
}.items():
    p = Path(path)
    report["kernel"][name] = p.read_text().strip() if p.exists() else "unavailable"

(COURSE / "reports").mkdir(exist_ok=True)
(COURSE / "reports" / "doctor.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(json.dumps(report, indent=2, sort_keys=True))
if not report["mandatory"]["python"]["ok"] or report["mandatory"]["go"]["status"] != "present":
    raise SystemExit(1)
