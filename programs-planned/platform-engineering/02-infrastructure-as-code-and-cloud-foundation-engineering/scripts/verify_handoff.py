from __future__ import annotations

import json
from pathlib import Path

from common import CAPSTONE, load_json, sha256


def verify(directory: Path) -> tuple[int, list[str]]:
    manifest = load_json(directory / "MANIFEST.json")
    errors: list[str] = []
    for row in manifest.get("files", []):
        path = directory / row["path"]
        if not path.is_file():
            errors.append(f"missing {row['path']}")
        elif sha256(path) != row["sha256"]:
            errors.append(f"digest mismatch {row['path']}")
        elif path.stat().st_size != int(row["bytes"]):
            errors.append(f"size mismatch {row['path']}")
    return len(manifest.get("files", [])), errors


def main() -> int:
    results = {}
    errors: list[str] = []
    for name in ("predecessor", "handoff"):
        count, current = verify(CAPSTONE / name)
        results[name] = {"files": count, "valid": not current, "errors": current}
        errors.extend(f"{name}: {error}" for error in current)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
