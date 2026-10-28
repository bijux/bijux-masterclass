#!/usr/bin/env python3
"""Build and verify a deterministic repository-ready ZIP for API Engineering."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSES = [
    "01-openapi-contract-engineering",
    "02-contract-driven-api-service-engineering",
    "03-api-security-engineering",
    "04-api-reliability-and-observability-engineering",
    "05-api-performance-capacity-and-traffic-engineering",
    "06-event-driven-api-engineering",
]
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def make_tool() -> str:
    return shutil.which("gmake") or shutil.which("make") or "make"


def run_make(root: Path, target: str) -> None:
    subprocess.run([make_tool(), target], cwd=root, check=True, text=True)


def verify_manifests(root: Path) -> None:
    run_make(root, "manifest-proof")
    for course in COURSES:
        subprocess.run(
            [make_tool(), "-C", str(root / course), "manifest-proof"],
            check=True,
            text=True,
        )


def manifested_files() -> list[Path]:
    manifest_path = ROOT / "MANIFEST.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = [ROOT / row["path"] for row in payload["files"]]
    files.extend([ROOT / "MANIFEST.json", ROOT / "MANIFEST.sha256"])
    missing = [str(path.relative_to(ROOT)) for path in files if not path.is_file()]
    if missing:
        raise RuntimeError(f"manifested release files are missing: {missing[:20]}")
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def write_archive(output: Path, prefix: str, files: list[Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.unlink(missing_ok=True)
    prefix = prefix.strip("/")
    with zipfile.ZipFile(
        temporary,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            member = f"{prefix}/{relative}" if prefix else relative
            info = zipfile.ZipInfo(member, date_time=FIXED_TIMESTAMP)
            info.create_system = 3
            info.external_attr = (stat.S_IMODE(path.stat().st_mode) & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            info.flag_bits |= 0x800
            archive.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    os.replace(temporary, output)


def inspect_archive(path: Path, prefix: str, expected_members: int) -> dict[str, Any]:
    prefix_parts = PurePosixPath(prefix.strip("/")).parts if prefix.strip("/") else ()
    names: list[str] = []
    executable_members = 0
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) != expected_members:
            raise RuntimeError(
                f"ZIP has {len(infos)} members; expected {expected_members}"
            )
        for info in infos:
            pure = PurePosixPath(info.filename)
            if pure.is_absolute() or ".." in pure.parts:
                raise RuntimeError(f"unsafe ZIP member: {info.filename}")
            if prefix_parts and pure.parts[: len(prefix_parts)] != prefix_parts:
                raise RuntimeError(f"ZIP member escaped prefix: {info.filename}")
            if info.date_time != FIXED_TIMESTAMP:
                raise RuntimeError(f"non-deterministic timestamp: {info.filename}")
            mode = stat.S_IMODE(info.external_attr >> 16)
            if mode & 0o111:
                executable_members += 1
            names.append(info.filename)
        if len(names) != len(set(names)):
            raise RuntimeError("ZIP contains duplicate member names")
        corrupt = archive.testzip()
        if corrupt is not None:
            raise RuntimeError(f"ZIP CRC failed for {corrupt}")
    return {
        "members": len(names),
        "uniqueMembers": len(set(names)),
        "safePaths": True,
        "fixedTimestamps": True,
        "crc": "passed",
        "executableMembers": executable_members,
    }


def extraction_proof(archive_path: Path, prefix: str) -> dict[str, Any]:
    normalized = prefix.strip("/")
    with tempfile.TemporaryDirectory(prefix="api-engineering-six-course-") as temporary:
        target = Path(temporary)
        with zipfile.ZipFile(archive_path) as archive:
            for info in archive.infolist():
                extracted = Path(archive.extract(info, target))
                mode = stat.S_IMODE(info.external_attr >> 16)
                if mode:
                    extracted.chmod(mode)
        extracted_root = target / normalized if normalized else target
        if not extracted_root.is_dir():
            raise RuntimeError(f"extracted program root is missing: {extracted_root}")
        verify_manifests(extracted_root)
        run_make(extracted_root, "release-proof")
        course_results: dict[str, str] = {}
        for course in COURSES:
            subprocess.run(
                [make_tool(), "-C", str(extracted_root / course), "core-proof"],
                check=True,
                text=True,
            )
            course_results[course] = "passed"
        run_make(extracted_root, "clean")
        verify_manifests(extracted_root)
        return {
            "root": normalized or ".",
            "initialManifestProof": "passed",
            "programReleaseProof": "passed",
            "courseCoreProofs": course_results,
            "postProofCleanup": "passed",
            "postCleanupManifestProof": "passed",
        }


def create(
    output: Path,
    prefix: str,
    checksum_path: Path | None,
    report_path: Path | None,
) -> dict[str, Any]:
    verify_manifests(ROOT)
    run_make(ROOT, "release-proof")
    files = manifested_files()
    output = output.resolve()

    write_archive(output, prefix, files)
    first_hash = sha256(output)
    with tempfile.TemporaryDirectory(prefix="api-engineering-rebuild-") as temporary:
        second = Path(temporary) / output.name
        write_archive(second, prefix, files)
        second_hash = sha256(second)
        if first_hash != second_hash or output.read_bytes() != second.read_bytes():
            raise RuntimeError("two deterministic ZIP builds produced different bytes")

    inspection = inspect_archive(output, prefix, len(files))
    extraction = extraction_proof(output, prefix)
    payload: dict[str, Any] = {
        "format": 2,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "program": "api-engineering",
        "courses": COURSES,
        "archive": output.name,
        "prefix": prefix.strip("/"),
        "files": len(files),
        "bytes": output.stat().st_size,
        "sha256": first_hash,
        "reproducibleSecondBuild": True,
        "archiveInspection": inspection,
        "cleanExtraction": extraction,
        "evidenceBoundary": {
            "dependencyLightProgramAndCourseProofs": "passed",
            "exactManifests": "passed",
            "environmentBackedProofs": (
                "Live PostgreSQL, broker, complete external CLI, strict documentation "
                "rendering, and representative load routes retain the explicit statuses "
                "recorded by each course. Absence is never converted into a pass."
            ),
        },
    }

    if checksum_path is not None:
        checksum_path = checksum_path.resolve()
        checksum_path.parent.mkdir(parents=True, exist_ok=True)
        checksum_path.write_text(f"{first_hash}  {output.name}\n", encoding="utf-8")
        payload["checksumFile"] = checksum_path.name
    if report_path is not None:
        report_path = report_path.resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        payload["reportFile"] = report_path.name

    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prefix", default="programs/api-engineering")
    parser.add_argument("--checksum", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    create(args.output, args.prefix, args.checksum, args.report)


if __name__ == "__main__":
    main()
