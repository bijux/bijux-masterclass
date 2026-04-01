#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()

    out = Path(args.out).resolve()
    base = out.parent.resolve()  # make paths relative to the manifest directory (portable)

    files = [Path(p).resolve() for p in args.files]

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(base))
        except Exception:
            # fall back to a stable-ish path
            return str(p)

    payload = {
        "schema_version": 2,
        "base": str(base),
        "files": [
            {"path": rel(p), "sha256": sha256_file(p)} for p in sorted(files, key=lambda x: rel(x))
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
