#!/usr/bin/env python3
"""Export the immutable Course 1 contract handoff after local proof succeeds."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
OUTPUT = CAPSTONE / "handoff"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    value.update(path.read_bytes())
    return value.hexdigest()


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    (OUTPUT / "spec" / "dist").mkdir(parents=True)

    copies = {
        CAPSTONE / "spec/openapi.yaml": OUTPUT / "spec/openapi.yaml",
        CAPSTONE / "spec/openapi-3.2.yaml": OUTPUT / "spec/openapi-3.2.yaml",
        CAPSTONE / "spec/dist/openapi.bundle.yaml": OUTPUT / "spec/dist/openapi.bundle.yaml",
        CAPSTONE / "spec/dist/operation-ledger.json": OUTPUT / "operation-ledger.json",
        CAPSTONE / "tests/conformance/behavioral-scenarios.yaml": OUTPUT / "behavioral-scenarios.yaml",
        CAPSTONE / "tests/security/scope-matrix.yaml": OUTPUT / "scope-matrix.yaml",
        CAPSTONE / "docs/contract-decisions.md": OUTPUT / "contract-decisions.md",
        CAPSTONE / "docs/operations.md": OUTPUT / "operations.md",
        CAPSTONE / "docs/architecture.md": OUTPUT / "predecessor-architecture.md",
        CAPSTONE / "docs/security-model.md": OUTPUT / "security-model.md",
        CAPSTONE / "docs/state-machine.md": OUTPUT / "state-machine.md",
    }
    for source, target in copies.items():
        if not source.is_file():
            raise SystemExit(f"required handoff source is missing: {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copytree(
        CAPSTONE / "tests/fixtures/schema",
        OUTPUT / "schema-fixtures",
    )

    (OUTPUT / "README.md").write_text(
        """# Course 1 → Course 2 handoff

This directory is the immutable public-contract baseline consumed by
**Contract-Driven API Service Engineering**. It represents public API **1.1.0**
using OpenAPI **3.1.2**, with an OpenAPI **3.2.0** frontier copy for standards
study.

Course 2 may change application, database, worker, storage, and release
mechanisms, but it may not silently weaken this baseline. The manifest makes
that constraint machine-checkable.

Regenerate only after Course 1's proof route passes.
""",
        encoding="utf-8",
    )

    files = []
    for path in sorted(OUTPUT.rglob("*")):
        if path.is_file() and path.name not in {"MANIFEST.json", "MANIFEST.sha256"}:
            files.append(
                {
                    "path": path.relative_to(OUTPUT).as_posix(),
                    "size": path.stat().st_size,
                    "sha256": digest(path),
                }
            )
    manifest = {
        "generated": "2026-08-05",
        "publicApiVersion": "1.1.0",
        "openapiSpecification": "3.1.2",
        "files": files,
    }
    manifest_path = OUTPUT / "MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUTPUT / "MANIFEST.sha256").write_text(
        f"{digest(manifest_path)}  MANIFEST.json\n",
        encoding="utf-8",
    )
    print(f"exported {len(files)} handoff files to {OUTPUT}")


if __name__ == "__main__":
    main()
