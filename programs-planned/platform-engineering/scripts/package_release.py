from __future__ import annotations

import argparse
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PREFIX = PurePosixPath("programs/platform-engineering")
FIXED_TIME = (2026, 8, 9, 0, 0, 0)


def inventory() -> list[Path]:
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    paths = [ROOT / row["path"] for row in manifest["files"]]
    paths.extend([ROOT / "MANIFEST.json", ROOT / "MANIFEST.sha256"])
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(f"missing package inputs: {missing[:5]}")
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def add_file(archive: zipfile.ZipFile, path: Path) -> None:
    rel = PurePosixPath(path.relative_to(ROOT).as_posix())
    member = str(PREFIX / rel)
    if member.startswith("/") or ".." in PurePosixPath(member).parts:
        raise SystemExit(f"unsafe archive member: {member}")
    info = zipfile.ZipInfo(member, FIXED_TIME)
    mode = path.stat().st_mode & 0o777
    info.create_system = 3
    info.external_attr = ((stat.S_IFREG | mode) & 0xFFFF) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", allowZip64=True) as archive:
        seen: set[str] = set()
        for path in inventory():
            member = str(PREFIX / PurePosixPath(path.relative_to(ROOT).as_posix()))
            if member in seen:
                raise SystemExit(f"duplicate member: {member}")
            seen.add(member)
            add_file(archive, path)
    print(f"created {output} with {len(seen)} files")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
