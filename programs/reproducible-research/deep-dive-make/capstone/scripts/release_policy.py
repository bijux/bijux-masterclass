"""Parse the capstone release package policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath


@dataclass(frozen=True)
class PackageMember:
    archive_path: PurePosixPath
    source_path: Path
    mode: int


@dataclass(frozen=True)
class InstallMapping:
    archive_path: PurePosixPath
    install_path: PurePosixPath
    mode: int


def _safe_relative_path(raw_path: str, *, field: str, line_number: int) -> PurePosixPath:
    path = PurePosixPath(raw_path)
    if not raw_path or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"line {line_number}: unsafe {field}: {raw_path!r}")
    return path


def read_package_policy(policy_path: Path) -> list[PackageMember]:
    """Return validated package members in archive-path order."""
    members: list[PackageMember] = []
    archive_paths: set[PurePosixPath] = set()
    source_paths: set[Path] = set()

    for line_number, raw_line in enumerate(
        policy_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line or raw_line.startswith("#"):
            continue

        fields = raw_line.split("\t")
        if len(fields) != 3:
            raise ValueError(
                f"line {line_number}: expected archive path, source path, and mode"
            )

        archive_path = _safe_relative_path(
            fields[0], field="archive path", line_number=line_number
        )
        source_path = Path(
            _safe_relative_path(fields[1], field="source path", line_number=line_number)
        )
        try:
            mode = int(fields[2], 8)
        except ValueError as error:
            raise ValueError(
                f"line {line_number}: invalid octal mode: {fields[2]!r}"
            ) from error
        if mode < 0 or mode > 0o7777:
            raise ValueError(f"line {line_number}: mode outside supported range")
        if archive_path in archive_paths:
            raise ValueError(f"line {line_number}: duplicate archive path: {archive_path}")
        if source_path in source_paths:
            raise ValueError(f"line {line_number}: duplicate source path: {source_path}")

        archive_paths.add(archive_path)
        source_paths.add(source_path)
        members.append(PackageMember(archive_path, source_path, mode))

    if not members:
        raise ValueError("package policy contains no members")
    return sorted(members, key=lambda member: member.archive_path.as_posix())


def read_install_policy(policy_path: Path) -> list[InstallMapping]:
    """Return validated install mappings in destination-path order."""
    mappings: list[InstallMapping] = []
    archive_paths: set[PurePosixPath] = set()
    install_paths: set[PurePosixPath] = set()

    for line_number, raw_line in enumerate(
        policy_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line or raw_line.startswith("#"):
            continue

        fields = raw_line.split("\t")
        if len(fields) != 3:
            raise ValueError(
                f"line {line_number}: expected archive path, install path, and mode"
            )

        archive_path = _safe_relative_path(
            fields[0], field="archive path", line_number=line_number
        )
        install_path = _safe_relative_path(
            fields[1], field="install path", line_number=line_number
        )
        try:
            mode = int(fields[2], 8)
        except ValueError as error:
            raise ValueError(
                f"line {line_number}: invalid octal mode: {fields[2]!r}"
            ) from error
        if mode < 0 or mode > 0o7777:
            raise ValueError(f"line {line_number}: mode outside supported range")
        if archive_path in archive_paths:
            raise ValueError(f"line {line_number}: duplicate archive path: {archive_path}")
        if install_path in install_paths:
            raise ValueError(f"line {line_number}: duplicate install path: {install_path}")

        archive_paths.add(archive_path)
        install_paths.add(install_path)
        mappings.append(InstallMapping(archive_path, install_path, mode))

    if not mappings:
        raise ValueError("install policy contains no mappings")
    return sorted(mappings, key=lambda mapping: mapping.install_path.as_posix())
