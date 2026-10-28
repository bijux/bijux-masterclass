from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .runtime_config import validate_runtime_config


def available() -> bool:
    return all(shutil.which(name) for name in ("unshare", "mount", "chroot")) and os.geteuid() == 0


def run_bundle(bundle: Path, state: Path, timeout: float = 10.0) -> dict[str, Any]:
    config = json.loads((bundle / "config.json").read_text())
    errors = validate_runtime_config(config)
    if errors:
        raise ValueError("invalid runtime configuration: " + "; ".join(errors))
    if not available():
        raise RuntimeError("mini runtime is a root-managed teaching harness requiring host root plus unshare, mount, and chroot; the workload UID/GID map to subordinate host IDs")
    rootfs = (bundle / config["root"]["path"]).resolve()
    state = state.resolve()
    state.mkdir(parents=True, exist_ok=True)
    # Namespace root maps to host root for this root-managed teaching harness.
    # Inner IDs 1..65535 map to host IDs 100000..165534, so inner 65532
    # owns the state directory as host 165531.
    os.chown(state, 100000 + 65532 - 1, 100000 + 65532 - 1)
    state.chmod(0o770)
    (rootfs / "proc").mkdir(parents=True, exist_ok=True)
    (rootfs / "tmp").mkdir(parents=True, exist_ok=True)
    (rootfs / "var/lib/atlas").mkdir(parents=True, exist_ok=True)
    script = r'''
set -eu
mount --make-rprivate /
mount --bind "$ROOTFS" "$ROOTFS"
mount -o remount,bind,ro "$ROOTFS"
mount -t tmpfs -o nosuid,nodev,mode=1777,size=16777216 tmpfs "$ROOTFS/tmp"
mount --bind "$STATE" "$ROOTFS/var/lib/atlas"
mount -o remount,bind,rw,nosuid,nodev "$ROOTFS/var/lib/atlas"
hostname atlas-probe
exec chroot --userspec=65532:65532 "$ROOTFS" /usr/local/bin/atlas-probe
'''
    env = dict(os.environ, ROOTFS=str(rootfs), STATE=str(state))
    completed = subprocess.run(
        ["unshare", "--user", "--map-users", "0:0:1", "--map-users", "1:100000:65535", "--map-groups", "0:0:1", "--map-groups", "1:100000:65535", "--mount", "--pid", "--uts", "--ipc", "--net", "--fork", "bash", "-c", script],
        text=True,
        capture_output=True,
        timeout=timeout,
        env=env,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"mini runtime failed ({completed.returncode}): {completed.stderr.strip()}"
        )
    return json.loads(completed.stdout)
