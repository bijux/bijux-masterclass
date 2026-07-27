#!/usr/bin/env python3
"""Rehearse installation from one accepted candidate below a controlled root."""

from __future__ import annotations

import argparse
import json
import os
import stat
import tarfile
from pathlib import Path, PurePosixPath

from release_policy import InstallMapping, read_install_policy, read_package_policy
from verify_release_candidate import sha256, verify_archive


def read_acceptance(report_path: Path, candidate: Path) -> dict[str, object]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    digest = sha256(candidate)
    if report.get("candidate") != candidate.name or report.get("sha256") != digest:
        raise ValueError("acceptance report does not name the candidate under rehearsal")
    checks = report.get("checks")
    if not isinstance(checks, dict) or not checks or set(checks.values()) != {"PASS"}:
        raise ValueError("candidate acceptance report contains an incomplete gate")
    return report


def validate_root(root: Path) -> Path:
    if not root.is_absolute():
        raise ValueError("install root must be absolute")
    if root == Path(root.anchor):
        raise ValueError("install root cannot be a filesystem root")
    if root.is_symlink():
        raise ValueError("install root cannot be a symbolic link")
    return root


def destination_for(root: Path, install_path: PurePosixPath) -> Path:
    destination = root.joinpath(*install_path.parts)
    destination.relative_to(root)
    return destination


def reject_unsafe_ancestors(root: Path, destination: Path) -> None:
    relative = destination.relative_to(root)
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"destination ancestor is a symbolic link: {current}")
        if current.exists() and not current.is_dir():
            raise ValueError(f"destination ancestor is not a directory: {current}")
    if destination.is_symlink() or (destination.exists() and not destination.is_file()):
        raise ValueError(f"destination is not a replaceable regular file: {destination}")


def read_payloads(
    candidate: Path, mappings: list[InstallMapping]
) -> dict[PurePosixPath, bytes]:
    expected = {mapping.archive_path for mapping in mappings}
    payloads: dict[PurePosixPath, bytes] = {}
    with tarfile.open(candidate, "r:gz") as archive:
        for info in archive.getmembers():
            path = PurePosixPath(info.name)
            if path not in expected:
                continue
            handle = archive.extractfile(info)
            if handle is None:
                raise ValueError(f"cannot read install payload: {path}")
            payloads[path] = handle.read()
    missing = sorted(path.as_posix() for path in expected - payloads.keys())
    if missing:
        raise ValueError(f"candidate is missing install payloads: {missing}")
    return payloads


def reject_unowned_files(root: Path, mappings: list[InstallMapping]) -> None:
    if not root.exists():
        return
    expected = {
        destination_for(root, mapping.install_path).relative_to(root).as_posix()
        for mapping in mappings
    }
    observed = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    unowned = sorted(observed - expected)
    if unowned:
        raise ValueError(f"install root contains unowned paths: {unowned}")


def apply_install(
    root: Path,
    mappings: list[InstallMapping],
    payloads: dict[PurePosixPath, bytes],
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for mapping in mappings:
        destination = destination_for(root, mapping.install_path)
        reject_unsafe_ancestors(root, destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        staged_output = destination.with_name(
            f".{destination.name}.install.{os.getpid()}"
        )
        try:
            with staged_output.open("xb") as handle:
                handle.write(payloads[mapping.archive_path])
            staged_output.chmod(mapping.mode)
            os.replace(staged_output, destination)
        finally:
            staged_output.unlink(missing_ok=True)


def snapshot(root: Path) -> list[dict[str, object]]:
    files: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"installed tree contains a symbolic link: {path}")
        if not path.is_file():
            continue
        files.append(
            {
                "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256(path),
            }
        )
    return files


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
    parser.add_argument("--acceptance", required=True)
    parser.add_argument("--package-policy", required=True)
    parser.add_argument("--install-policy", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--report", required=True)
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    candidate = Path(args.candidate)
    acceptance = read_acceptance(Path(args.acceptance), candidate)
    package_members = read_package_policy(Path(args.package_policy))
    verify_archive(candidate, package_members)

    mappings = read_install_policy(Path(args.install_policy))
    packaged_paths = {member.archive_path for member in package_members}
    unmapped = sorted(
        mapping.archive_path.as_posix()
        for mapping in mappings
        if mapping.archive_path not in packaged_paths
    )
    if unmapped:
        raise ValueError(f"install policy names unpackaged members: {unmapped}")

    root = validate_root(Path(args.root))
    reject_unowned_files(root, mappings)
    payloads = read_payloads(candidate, mappings)
    apply_install(root, mappings, payloads)
    first_snapshot = snapshot(root)
    apply_install(root, mappings, payloads)
    second_snapshot = snapshot(root)
    if first_snapshot != second_snapshot:
        raise ValueError("install tree did not converge after the second application")

    write_report(
        Path(args.report),
        {
            "candidate": candidate.name,
            "checks": {
                "accepted_candidate": "PASS",
                "contained_destinations": "PASS",
                "install_convergence": "PASS",
                "install_modes": "PASS",
            },
            "files": second_snapshot,
            "install_root": root.as_posix(),
            "sha256": acceptance["sha256"],
        },
    )


def main() -> int:
    try:
        run()
    except (OSError, tarfile.TarError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1
    print("PASS: accepted candidate converges below the install root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
