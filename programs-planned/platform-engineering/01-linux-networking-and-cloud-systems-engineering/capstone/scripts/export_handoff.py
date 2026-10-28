from __future__ import annotations

import hashlib
import json
from pathlib import Path


def main() -> int:
    cap = Path(__file__).resolve().parents[1]
    handoff = cap / "handoff"
    files = sorted(p for p in handoff.rglob("*") if p.is_file() and p.name not in {"MANIFEST.json", "MANIFEST.sha256"})
    entries = []
    for path in files:
        rel = path.relative_to(handoff).as_posix()
        entries.append({"path": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    manifest = {"schemaVersion": 1, "profile": "course-01-to-02", "files": entries}
    raw = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    (handoff / "MANIFEST.json").write_text(raw)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    (handoff / "MANIFEST.sha256").write_text(f"{digest}  MANIFEST.json\n")
    print(f"exported {len(entries)} handoff files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
