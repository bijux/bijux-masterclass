#!/usr/bin/env python3
"""Create a reproducible release archive.

Usage:
  scripts/mkdist.py OUT.tar.gz <path> [<path> ...]
  scripts/mkdist.py --policy POLICY.tsv --output OUT.tar.gz
"""

from __future__ import annotations

import argparse
import gzip
import os
import stat
import sys
import tarfile
from pathlib import Path
from typing import Iterable

from release_policy import PackageMember, read_package_policy

# Fixed timestamp to avoid embedding "now" into the archive.
FIXED_MTIME = 946684800  # 2000-01-01T00:00:00Z


def iter_paths(root: Path) -> Iterable[Path]:
    """Yield all paths under root in a stable order, including root."""
    if root.is_dir():
        yield root
        for p in sorted(root.rglob("*")):
            yield p
    else:
        yield root


def add_path(tf: tarfile.TarFile, p: Path, arcname: str) -> None:
    """Add p into tf with normalized metadata."""
    st = p.lstat()

    ti = tarfile.TarInfo(name=arcname)
    ti.mtime = FIXED_MTIME
    ti.uid = 0
    ti.gid = 0
    ti.uname = "root"
    ti.gname = "root"

    ti.mode = stat.S_IMODE(st.st_mode)

    if p.is_symlink():
        ti.type = tarfile.SYMTYPE
        ti.linkname = os.readlink(p)
        ti.size = 0
        tf.addfile(ti)
        return

    if p.is_dir():
        ti.type = tarfile.DIRTYPE
        ti.size = 0
        if not ti.name.endswith("/"):
            ti.name += "/"
        tf.addfile(ti)
        return

    if p.is_file():
        ti.type = tarfile.REGTYPE
        ti.size = st.st_size
        with p.open("rb") as fh:
            tf.addfile(ti, fileobj=fh)
        return

    raise RuntimeError(f"Unsupported file type: {p}")


def add_policy_member(tf: tarfile.TarFile, member: PackageMember, root: Path) -> None:
    """Add one policy-governed regular file with declared archive metadata."""
    source = member.source_path
    resolved_source = source.resolve()
    try:
        resolved_source.relative_to(root)
    except ValueError as error:
        raise ValueError(f"source path escapes project root: {source}") from error
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"release source must be a regular file: {source}")

    info = tarfile.TarInfo(name=member.archive_path.as_posix())
    info.mtime = FIXED_MTIME
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mode = member.mode
    info.type = tarfile.REGTYPE
    info.size = source.stat().st_size
    with source.open("rb") as handle:
        tf.addfile(info, fileobj=handle)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy")
    parser.add_argument("--output")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args(argv[1:])

    if args.policy:
        if not args.output or args.paths:
            parser.error("--policy requires --output and no positional paths")
    elif args.output or len(args.paths) < 2:
        parser.error("provide OUT.tar.gz followed by one or more paths")
    return args


def write_archive(
    output: Path,
    *,
    inputs: list[Path] | None = None,
    policy_members: list[PackageMember] | None = None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with gzip.GzipFile(filename=str(output), mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tf:
            cwd = Path.cwd().resolve()
            if policy_members is not None:
                for member in policy_members:
                    add_policy_member(tf, member, cwd)
            else:
                assert inputs is not None
                for input_path in inputs:
                    for path in iter_paths(input_path):
                        relative_path = path.resolve().relative_to(cwd)
                        add_path(tf, path, relative_path.as_posix())


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.policy:
        output = Path(args.output)
        policy_members = read_package_policy(Path(args.policy))
        write_archive(output, policy_members=policy_members)
    else:
        output = Path(args.paths[0])
        inputs = [Path(path) for path in args.paths[1:]]
        write_archive(output, inputs=inputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
