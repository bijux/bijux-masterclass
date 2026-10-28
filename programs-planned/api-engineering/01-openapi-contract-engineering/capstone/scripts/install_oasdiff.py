#!/usr/bin/env python3
"""Install the course-pinned oasdiff binary into .tools/bin.

The installer follows the upstream release naming convention, verifies the
published SHA-256 checksum, extracts only the expected executable, and never
writes outside the course-local tools directory.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import platform
import re
import stat
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]
VERSIONS = COURSE / "tool-versions.json"
TOOLS_BIN = COURSE / ".tools" / "bin"
REPOSITORY = "oasdiff/oasdiff"


class InstallError(RuntimeError):
    """Raised when the pinned native tool cannot be installed safely."""


def pinned_version() -> str:
    payload = json.loads(VERSIONS.read_text(encoding="utf-8"))
    try:
        return str(payload["native_tools"]["oasdiff"])
    except (KeyError, TypeError) as exc:
        raise InstallError("native_tools.oasdiff is missing from tool-versions.json") from exc


def platform_triplet(
    system: str | None = None,
    machine: str | None = None,
) -> tuple[str, str]:
    system_name = (system or platform.system()).lower()
    machine_name = (machine or platform.machine()).lower()
    if system_name == "darwin":
        return "darwin", "all"
    if system_name != "linux":
        raise InstallError(f"oasdiff automatic installation does not support {system_name!r}")
    architecture = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "x64": "amd64",
        "i386": "i386",
        "i686": "i386",
        "aarch64": "arm64",
        "arm64": "arm64",
        "armv6l": "arm64",
    }.get(machine_name)
    if architecture is None:
        raise InstallError(f"oasdiff automatic installation does not support {machine_name!r}")
    return "linux", architecture


def asset_name(version: str, system: str | None = None, machine: str | None = None) -> str:
    os_name, architecture = platform_triplet(system, machine)
    return f"oasdiff_{version}_{os_name}_{architecture}.tar.gz"


def release_url(version: str, filename: str) -> str:
    return f"https://github.com/{REPOSITORY}/releases/download/v{version}/{filename}"


def _download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "bijux-openapi-course-setup"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            return response.read()
    except OSError as exc:
        raise InstallError(f"download failed: {url}: {exc}") from exc


def parse_checksum(checksums: str, filename: str) -> str:
    pattern = re.compile(rf"^([0-9a-fA-F]{{64}})\s+\*?{re.escape(filename)}$")
    for line in checksums.splitlines():
        match = pattern.match(line.strip())
        if match:
            return match.group(1).lower()
    raise InstallError(f"published checksum not found for {filename}")


def verify_checksum(content: bytes, expected: str) -> None:
    actual = hashlib.sha256(content).hexdigest()
    if actual != expected.lower():
        raise InstallError(f"checksum mismatch: expected {expected.lower()}, received {actual}")


def extract_executable(archive: bytes, destination: Path) -> None:
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
            candidates = [member for member in bundle.getmembers() if Path(member.name).name == "oasdiff"]
            if len(candidates) != 1 or not candidates[0].isfile():
                raise InstallError("release archive does not contain exactly one regular oasdiff file")
            source = bundle.extractfile(candidates[0])
            if source is None:
                raise InstallError("unable to read oasdiff from release archive")
            payload = source.read()
    except (tarfile.TarError, OSError) as exc:
        raise InstallError(f"invalid oasdiff release archive: {exc}") from exc

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(payload)
    temporary.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    temporary.replace(destination)


def installed_version(executable: Path) -> str | None:
    if not executable.is_file() or not os.access(executable, os.X_OK):
        return None
    try:
        result = subprocess.run(
            [str(executable), "--version"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return (result.stdout or result.stderr).strip() or None


def main() -> int:
    version = pinned_version()
    executable = TOOLS_BIN / "oasdiff"
    observed = installed_version(executable)
    if observed and version in observed:
        print(f"PASS oasdiff {version} already installed — {executable}")
        return 0

    filename = asset_name(version)
    checksums = _download(release_url(version, "checksums.txt")).decode("utf-8")
    expected = parse_checksum(checksums, filename)
    archive = _download(release_url(version, filename))
    verify_checksum(archive, expected)
    extract_executable(archive, executable)

    observed = installed_version(executable)
    if observed is None or version not in observed:
        raise InstallError(f"installed executable did not report pinned version {version}: {observed}")
    print(f"PASS installed {observed} — {executable}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InstallError as error:
        raise SystemExit(f"oasdiff setup failed: {error}") from error
