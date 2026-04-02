#!/usr/bin/env python3
"""Build a deterministic tar.gz bundle from tracked files only."""

from __future__ import annotations

import argparse
import gzip
from pathlib import Path
import subprocess
import tarfile


def tracked_files(repo_root: Path, source_spec: str) -> list[Path]:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "-z", "--", source_spec],
        check=True,
        capture_output=True,
    )
    entries = [item for item in proc.stdout.decode("utf-8").split("\0") if item]
    return [repo_root / entry for entry in entries]


def build_bundle(repo_root: Path, source_dir: Path, output_path: Path, prefix: str) -> int:
    source_spec = source_dir.relative_to(repo_root).as_posix()
    files = tracked_files(repo_root, source_spec)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("wb") as raw_stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_stream, mtime=0) as gzip_stream:
            with tarfile.open(fileobj=gzip_stream, mode="w", format=tarfile.PAX_FORMAT) as tar_stream:
                for path in files:
                    arcname = Path(prefix) / path.relative_to(source_dir)
                    tarinfo = tar_stream.gettarinfo(str(path), arcname=arcname.as_posix())
                    tarinfo.uid = 0
                    tarinfo.gid = 0
                    tarinfo.uname = ""
                    tarinfo.gname = ""
                    tarinfo.mtime = 0
                    if tarinfo.isfile():
                        with path.open("rb") as handle:
                            tar_stream.addfile(tarinfo, handle)
                    else:
                        tar_stream.addfile(tarinfo)
    return len(files)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, help="Repository root containing the git metadata")
    parser.add_argument("--source-dir", required=True, help="Tracked directory to bundle")
    parser.add_argument("--output", required=True, help="Output .tar.gz path")
    parser.add_argument("--prefix", help="Top-level directory name inside the archive")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    source_dir = Path(args.source_dir).resolve()
    output_path = Path(args.output).resolve()

    if repo_root not in source_dir.parents and repo_root != source_dir:
        raise SystemExit(f"source directory {source_dir} is not inside repository root {repo_root}")

    prefix = args.prefix or source_dir.name
    file_count = build_bundle(repo_root, source_dir, output_path, prefix)
    print(f"wrote {output_path} with {file_count} tracked files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
