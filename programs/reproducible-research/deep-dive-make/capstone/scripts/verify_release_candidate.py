#!/usr/bin/env python3
"""Verify one existing release candidate without rebuilding it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tarfile
from pathlib import Path, PurePosixPath

from release_policy import PackageMember, read_package_policy


FIXED_MTIME = 946684800


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_expected_identity(checksum_path: Path, candidate: Path) -> str:
    fields = checksum_path.read_text(encoding="utf-8").strip().split()
    if len(fields) != 2:
        raise ValueError("checksum sidecar must contain one digest and one filename")
    expected_digest, expected_name = fields
    if expected_name != candidate.name:
        raise ValueError(
            f"checksum names {expected_name!r}, not candidate {candidate.name!r}"
        )
    if len(expected_digest) != 64 or any(
        character not in "0123456789abcdef" for character in expected_digest
    ):
        raise ValueError("checksum sidecar does not contain a lowercase SHA-256 digest")
    return expected_digest


def validate_member_path(raw_path: str) -> PurePosixPath:
    path = PurePosixPath(raw_path)
    if not raw_path or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe archive path: {raw_path!r}")
    return path


def verify_archive(
    candidate: Path, policy_members: list[PackageMember]
) -> dict[str, object]:
    expected = {member.archive_path: member for member in policy_members}
    observed: dict[PurePosixPath, tarfile.TarInfo] = {}

    with tarfile.open(candidate, "r:gz") as archive:
        for info in archive.getmembers():
            path = validate_member_path(info.name)
            if path in observed:
                raise ValueError(f"duplicate archive member: {path}")
            if not info.isfile():
                raise ValueError(f"archive member is not a regular file: {path}")
            observed[path] = info

    missing = sorted(path.as_posix() for path in expected.keys() - observed.keys())
    unexpected = sorted(path.as_posix() for path in observed.keys() - expected.keys())
    if missing or unexpected:
        raise ValueError(
            f"member policy mismatch: missing={missing}, unexpected={unexpected}"
        )

    for path, member in expected.items():
        info = observed[path]
        if info.mode != member.mode:
            raise ValueError(
                f"mode mismatch for {path}: expected {member.mode:04o}, "
                f"observed {info.mode:04o}"
            )
        if (info.uid, info.gid, info.uname, info.gname) != (0, 0, "root", "root"):
            raise ValueError(f"ownership metadata mismatch for {path}")
        if info.mtime != FIXED_MTIME:
            raise ValueError(f"modification time mismatch for {path}")

    return {
        "member_count": len(observed),
        "members": sorted(path.as_posix() for path in observed),
    }


def write_report(output: Path, report: dict[str, object]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    staged_output = output.with_name(f".{output.name}.evidence.{os.getpid()}")
    try:
        staged_output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        os.replace(staged_output, output)
    finally:
        staged_output.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--checksum", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--report", required=True)
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    candidate = Path(args.candidate)
    checksum_path = Path(args.checksum)
    policy_path = Path(args.policy)

    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError(f"candidate is not a regular file: {candidate}")
    expected_digest = read_expected_identity(checksum_path, candidate)
    observed_digest = sha256(candidate)
    if observed_digest != expected_digest:
        raise ValueError(
            f"candidate identity mismatch: expected {expected_digest}, "
            f"observed {observed_digest}"
        )

    archive_report = verify_archive(candidate, read_package_policy(policy_path))
    write_report(
        Path(args.report),
        {
            "candidate": candidate.name,
            "checks": {
                "extraction_safety": "PASS",
                "identity": "PASS",
                "member_metadata": "PASS",
                "member_policy": "PASS",
                "member_types": "PASS",
            },
            "member_count": archive_report["member_count"],
            "members": archive_report["members"],
            "sha256": observed_digest,
        },
    )


def main() -> int:
    try:
        run()
    except (OSError, tarfile.TarError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1
    print("PASS: release candidate satisfies identity and package policy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
