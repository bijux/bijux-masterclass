#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from spec_tools import SPEC_DIR, bundle_document, write_yaml


def main() -> int:
    document = bundle_document(SPEC_DIR / "openapi.yaml")
    document["info"]["title"] = "Analysis Runs API — Client Generation View"
    document["info"]["x-derived-view"] = "client-generation"
    document.pop("webhooks", None)
    document["paths"].pop("/internal/diagnostics", None)
    document["paths"].pop("/analysis-runs/{runId}/events", None)
    run_create = document["paths"]["/analysis-runs"]["post"]
    run_create.pop("callbacks", None)
    tags = document.get("tags", [])
    document["tags"] = [tag for tag in tags if tag.get("name") not in {"Internal"}]
    output = SPEC_DIR / "dist/openapi.client.yaml"
    write_yaml(output, document)
    print(f"PASS client generation view — {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
