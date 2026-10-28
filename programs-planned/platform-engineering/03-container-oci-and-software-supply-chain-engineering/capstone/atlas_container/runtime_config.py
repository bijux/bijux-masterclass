from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any

_REQUIRED_NAMESPACES = {"pid", "mount", "uts", "ipc", "network", "user"}
_FORBIDDEN_BIND_SOURCES = {
    "/",
    "/proc",
    "/sys",
    "/dev",
    "/etc",
    "/run/containerd/containerd.sock",
    "/run/podman/podman.sock",
    "/var/run/docker.sock",
}
_ALLOWED_WRITABLE_DESTINATIONS = {"/tmp", "/var/lib/atlas"}


def _mapping_covers(mappings: list[dict[str, Any]], container_id: int) -> bool:
    for mapping in mappings:
        start = mapping.get("containerID")
        size = mapping.get("size")
        if isinstance(start, int) and isinstance(size, int) and size > 0:
            if start <= container_id < start + size:
                return True
    return False


def validate_runtime_config(config: dict[str, Any]) -> list[str]:
    """Validate Atlas's strict OCI runtime profile.

    This is a course policy validator, not an OCI Runtime Specification
    conformance suite. It checks the guarantees Atlas relies on.
    """

    errors: list[str] = []
    if config.get("ociVersion") != "1.3.0":
        errors.append("Atlas runtime profile requires OCI Runtime Spec 1.3.0")

    process = config.get("process", {})
    root = config.get("root", {})
    linux = config.get("linux", {})
    user = process.get("user", {})
    uid = user.get("uid")
    gid = user.get("gid")
    if not isinstance(uid, int) or isinstance(uid, bool) or uid <= 0:
        errors.append("runtime process must not run as UID 0 and must use a positive UID")
    if not isinstance(gid, int) or isinstance(gid, bool) or gid <= 0:
        errors.append("runtime process must use a positive non-root GID")
    args = process.get("args")
    if not isinstance(args, list) or not args or not isinstance(args[0], str):
        errors.append("runtime process requires an executable argument vector")
    elif not args[0].startswith("/"):
        errors.append("runtime executable must use an absolute path")
    if not process.get("noNewPrivileges", False):
        errors.append("noNewPrivileges must be true")

    capabilities = process.get("capabilities", {})
    for set_name in ("bounding", "effective", "permitted", "inheritable", "ambient"):
        if capabilities.get(set_name):
            errors.append(f"capability set {set_name} must be empty")

    root_path = root.get("path")
    if not isinstance(root_path, str) or not root_path or root_path.startswith("/"):
        errors.append("root path must be a non-empty relative bundle path")
    elif ".." in PurePosixPath(root_path).parts:
        errors.append("root path must not traverse outside the bundle")
    if not root.get("readonly", False):
        errors.append("root filesystem must be read-only")

    namespace_entries = linux.get("namespaces", [])
    namespaces = [entry.get("type") for entry in namespace_entries if isinstance(entry, dict)]
    if len(namespaces) != len(set(namespaces)):
        errors.append("runtime namespace types must not be duplicated")
    missing = sorted(_REQUIRED_NAMESPACES - set(namespaces))
    if missing:
        errors.append("missing namespaces: " + ", ".join(missing))

    uid_mappings = linux.get("uidMappings", [])
    gid_mappings = linux.get("gidMappings", [])
    if isinstance(uid, int) and not _mapping_covers(uid_mappings, uid):
        errors.append("UID mapping does not cover the workload UID")
    if isinstance(gid, int) and not _mapping_covers(gid_mappings, gid):
        errors.append("GID mapping does not cover the workload GID")
    for label, mappings, container_id in (
        ("UID", uid_mappings, uid),
        ("GID", gid_mappings, gid),
    ):
        if isinstance(container_id, int):
            for mapping in mappings:
                start = mapping.get("containerID")
                host = mapping.get("hostID")
                size = mapping.get("size")
                if (
                    isinstance(start, int)
                    and isinstance(host, int)
                    and isinstance(size, int)
                    and start <= container_id < start + size
                    and host + (container_id - start) == 0
                ):
                    errors.append(f"workload {label} must not map to host ID 0")

    resources = linux.get("resources", {})
    memory_limit = resources.get("memory", {}).get("limit")
    pids_limit = resources.get("pids", {}).get("limit")
    cpu = resources.get("cpu", {})
    if not isinstance(memory_limit, int) or isinstance(memory_limit, bool) or memory_limit <= 0:
        errors.append("positive memory limit is required")
    if not isinstance(pids_limit, int) or isinstance(pids_limit, bool) or pids_limit <= 0:
        errors.append("positive PID limit is required")
    if not isinstance(cpu.get("quota"), int) or cpu.get("quota", 0) <= 0:
        errors.append("positive CPU quota is required")
    if not isinstance(cpu.get("period"), int) or cpu.get("period", 0) <= 0:
        errors.append("positive CPU period is required")

    destinations: set[str] = set()
    for mount in config.get("mounts", []):
        if not isinstance(mount, dict):
            errors.append("mount entries must be objects")
            continue
        source = mount.get("source")
        destination = mount.get("destination")
        if not isinstance(destination, str) or not destination.startswith("/"):
            errors.append("mount destination must be an absolute path")
            continue
        if destination in destinations:
            errors.append(f"duplicate mount destination: {destination}")
        destinations.add(destination)
        if source in _FORBIDDEN_BIND_SOURCES or destination in {
            "/var/run/docker.sock",
            "/run/containerd/containerd.sock",
            "/run/podman/podman.sock",
        }:
            errors.append(f"forbidden mount: {source} -> {destination}")
        options = set(mount.get("options", []))
        writable = "rw" in options or ("ro" not in options and mount.get("type") in {"bind", "tmpfs"})
        if writable and destination not in _ALLOWED_WRITABLE_DESTINATIONS:
            errors.append(f"unexpected writable mount destination: {destination}")
    return errors


def atlas_runtime_config(
    rootfs: str = "rootfs",
    executable: str = "/usr/local/bin/atlas-probe",
) -> dict[str, Any]:
    empty_caps = {
        name: []
        for name in ("bounding", "effective", "permitted", "inheritable", "ambient")
    }
    # The checked mini-runtime is a root-managed teaching harness. Namespace
    # root maps to host root so the harness can construct mounts in restricted
    # CI, while workload IDs 1..65535 map to subordinate host IDs. This is not
    # evidence of a fully rootless runtime architecture.
    subordinate_mapping = [
        {"containerID": 0, "hostID": 0, "size": 1},
        {"containerID": 1, "hostID": 100000, "size": 65535},
    ]
    return {
        "ociVersion": "1.3.0",
        "process": {
            "terminal": False,
            "user": {"uid": 65532, "gid": 65532},
            "args": [executable],
            "env": ["PATH=/usr/local/bin:/usr/bin:/bin", "ATLAS_RELEASE=1.0.0"],
            "cwd": "/",
            "capabilities": empty_caps,
            "noNewPrivileges": True,
        },
        "root": {"path": rootfs, "readonly": True},
        "hostname": "atlas-probe",
        "mounts": [
            {
                "destination": "/proc",
                "type": "proc",
                "source": "proc",
                "options": ["nosuid", "noexec", "nodev", "ro"],
            },
            {
                "destination": "/tmp",
                "type": "tmpfs",
                "source": "tmpfs",
                "options": ["nosuid", "nodev", "mode=1777", "size=16777216", "rw"],
            },
            {
                "destination": "/var/lib/atlas",
                "type": "bind",
                "source": "state",
                "options": ["rbind", "rw", "nosuid", "nodev"],
            },
        ],
        "linux": {
            "namespaces": [
                {"type": item}
                for item in ("pid", "mount", "uts", "ipc", "network", "user")
            ],
            "uidMappings": subordinate_mapping,
            "gidMappings": subordinate_mapping,
            "resources": {
                "memory": {"limit": 134217728},
                "pids": {"limit": 64},
                "cpu": {"quota": 50000, "period": 100000},
            },
            "maskedPaths": ["/proc/kcore", "/proc/keys", "/proc/timer_list"],
            "readonlyPaths": [
                "/proc/asound",
                "/proc/bus",
                "/proc/fs",
                "/proc/irq",
                "/proc/sys",
                "/proc/sysrq-trigger",
            ],
        },
    }
