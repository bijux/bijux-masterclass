from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


def build_search_index(docs_root: Path) -> list[dict[str, Any]]:
    """Build a deterministic, dependency-light search index for Markdown docs."""
    entries: list[dict[str, Any]] = []
    for path in sorted(docs_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = next(
            (
                line[2:].strip()
                for line in text.splitlines()
                if line.startswith("# ")
            ),
            path.stem,
        )
        tokens = sorted(
            {
                token.lower().strip(".,:;`()[]{}")
                for token in text.split()
                if len(token) >= 3
            }
        )
        entries.append(
            {
                "path": str(path.relative_to(docs_root)),
                "title": title,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "tokens": tokens,
            }
        )
    return entries


def search(
    index: Iterable[Mapping[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    """Return deterministic token-intersection search results."""
    terms = {term.lower() for term in query.split() if term}
    scored: list[tuple[int, dict[str, Any]]] = []
    for entry in index:
        score = len(terms & set(entry["tokens"]))
        if score:
            scored.append((score, dict(entry)))
    return [
        entry
        for _, entry in sorted(
            scored,
            key=lambda item: (-item[0], item[1]["path"]),
        )
    ]


def write_portal(
    index: list[dict[str, Any]],
    catalog_summary: Mapping[str, Any],
    destination: Path,
) -> None:
    """Write a deterministic static portal artifact."""
    destination.mkdir(parents=True, exist_ok=True)
    payload = {
        "portalVersion": "1.0",
        "catalog": dict(catalog_summary),
        "documents": index,
    }
    (destination / "portal.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    rows = "\n".join(
        "<li><strong>"
        + html.escape(str(entry["title"]))
        + "</strong> — "
        + html.escape(str(entry["path"]))
        + "</li>"
        for entry in index
    )
    page = (
        "<!doctype html>\n"
        "<meta charset='utf-8'>\n"
        "<title>Analysis API Platform</title>\n"
        "<h1>Analysis API Platform</h1>\n"
        f"<ul>{rows}</ul>\n"
    )
    (destination / "index.html").write_text(page, encoding="utf-8")
