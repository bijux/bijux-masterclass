#!/usr/bin/env python3
"""Create a reproducible dist.tar.gz.

Usage:
  scripts/mkdist.py OUT.tar.gz <path> [<path> ...]
"""

from __future__ import annotations

import gzip
import os
import stat
import sys
import tarfile
from pathlib import Path
from typing import Iterable

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


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    out = Path(argv[1])
    inputs = [Path(a) for a in argv[2:]]

    out.parent.mkdir(parents=True, exist_ok=True)

    # gzip header also has an mtime; fix it to 0.
    with gzip.GzipFile(filename=str(out), mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tf:
            cwd = Path.cwd().resolve()
            for inp in inputs:
                for p in iter_paths(inp):
                    rel = p.resolve().relative_to(cwd)
                    add_path(tf, p, rel.as_posix())

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
