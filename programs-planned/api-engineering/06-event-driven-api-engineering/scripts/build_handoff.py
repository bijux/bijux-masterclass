#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import stat

ROOT = Path(__file__).resolve().parents[1]
CAPSTONE = ROOT / "capstone"
HANDOFF = CAPSTONE / "handoff"

if HANDOFF.exists():
    shutil.rmtree(HANDOFF)
HANDOFF.mkdir(parents=True)
shutil.copytree(CAPSTONE / "contracts", HANDOFF / "contracts")

copies = {
    "event-case": [
        "event-profile.json", "message-taxonomy.yaml", "channel-policy.yaml",
        "compatibility-policy.yaml", "consumer-catalog.yaml",
    ],
    "migrations": [
        "010_event_outbox_inbox.sql", "011_event_replay_dead_letters.sql",
        "012_event_contract_catalog.sql",
    ],
    "replay": ["replay-policy.yaml", "example-plan.yaml"],
    "security": ["producer-grants.yaml"],
    "stream-processing": ["window-policy.yaml"],
}
for directory, names in copies.items():
    source_directory = CAPSTONE / ("database/migrations" if directory == "migrations" else directory)
    for name in names:
        target = HANDOFF / directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_directory / name, target)
shutil.copytree(CAPSTONE / "shared/vectors", HANDOFF / "vectors")

release = {
    "eventApi": "1.0",
    "asyncapi": "3.1.0",
    "cloudEvents": "1.0",
    "eventProfile": "1.0",
    "publicHttpApi": "1.2",
    "migrationHead": "012",
    "contract": "contracts/asyncapi.yaml",
    "catalog": "contracts/event-catalog.yaml",
    "evidenceBoundary": (
        "Dependency-light semantics are verified; live broker and PostgreSQL "
        "routes remain environment-backed."
    ),
}
(HANDOFF / "releases").mkdir()
(HANDOFF / "releases/event-1.0.json").write_text(
    json.dumps(release, indent=2) + "\n", encoding="utf-8"
)
(HANDOFF / "README.md").write_text(
    "# Course 6 → Course 7 handoff\n\n"
    "This immutable package carries the governed event API into the next API "
    "Engineering course. It preserves HTTP API 1.2 and adds Event API 1.0, "
    "AsyncAPI 3.1.0, CloudEvents 1.0, event profile 1.0, and database revisions "
    "010–012.\n\n"
    "The next course may add a typed RPC boundary, but it must not silently "
    "change event meaning, partition identity, replay policy, or consumer effect "
    "identity.\n",
    encoding="utf-8",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


files = []
for path in sorted(HANDOFF.rglob("*")):
    if path.is_file() and path.name not in {"MANIFEST.json", "MANIFEST.sha256"}:
        files.append({
            "path": path.relative_to(HANDOFF).as_posix(),
            "size": path.stat().st_size,
            "sha256": sha256(path),
            "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
        })
manifest = {
    "schema": "bijux-handoff-manifest-1",
    "handoff": "course-6-to-course-7",
    "files": files,
}
manifest_path = HANDOFF / "MANIFEST.json"
manifest_path.write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
(HANDOFF / "MANIFEST.sha256").write_text(
    f"{sha256(manifest_path)}  MANIFEST.json\n", encoding="utf-8"
)
print(f"wrote Course 6 handoff with {len(files)} files")
