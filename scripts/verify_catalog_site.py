"""Verify owned article hyperlinks against the selected rendered catalog tree."""
from __future__ import annotations

import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Article(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "article":
            self.depth += 1
        if self.depth and tag in ("a", "area") and values.get("href"):
            self.links.append(values["href"])

    def handle_endtag(self, tag):
        if tag == "article":
            self.depth = max(0, self.depth - 1)


def inspect_catalog(site: Path, site_url: str) -> dict:
    site = site.resolve()
    base = urlsplit(site_url)
    if not site.is_dir() or not (site / "index.html").is_file():
        raise ValueError("selected catalog site is missing its root page")
    if base.scheme not in ("https", "http") or not base.netloc or not base.path.endswith("/"):
        raise ValueError("catalog site_url must be an absolute directory URL")
    pages = {}
    page_hashes = {}
    initial_paths = tuple(sorted(site.rglob("*")))
    initial_kinds = {path: (path.is_dir(), path.is_file(), path.is_symlink()) for path in initial_paths}
    for path in sorted(site.rglob("*.html")):
        content = path.read_bytes()
        parser = Article()
        parser.feed(content.decode("utf-8"))
        pages[path.resolve()] = parser
        page_hashes[path] = hashlib.sha256(content).hexdigest()
    errors = []
    references = 0
    destinations = {}
    for path, page in pages.items():
        relative = path.relative_to(site).as_posix()
        route = "" if relative == "index.html" else relative[:-10] if relative.endswith("/index.html") else relative
        for href in page.links:
            references += 1
            destination = urlsplit(urljoin(site_url + route, href))
            if destination.scheme not in ("http", "https") or destination.netloc != base.netloc or not destination.path.startswith(base.path):
                continue
            destination_path = unquote(destination.path[len(base.path):])
            if destination_path not in destinations:
                target = (site / destination_path).resolve()
                if destination.path.endswith("/") or target.is_dir():
                    target /= "index.html"
                destinations[destination_path] = (target, target.is_relative_to(site) and target.is_file())
            target, exists = destinations[destination_path]
            if not target.is_relative_to(site):
                errors.append({"page": relative, "href": href, "reason": "destination escapes selected catalog"})
                continue
            if not exists:
                errors.append({"page": relative, "href": href, "reason": "missing public destination"})
            elif destination.fragment and target in pages and unquote(destination.fragment) not in pages[target].ids:
                errors.append({"page": relative, "href": href, "reason": "missing public anchor"})
    final_paths = tuple(sorted(site.rglob("*")))
    final_kinds = {path: (path.is_dir(), path.is_file(), path.is_symlink()) for path in final_paths}
    if final_paths != initial_paths or final_kinds != initial_kinds:
        raise ValueError("selected catalog layout changed during verification")
    files = []
    for path in final_paths:
        if not path.is_file():
            continue
        content = path.read_bytes()
        content_sha256 = hashlib.sha256(content).hexdigest()
        if path in page_hashes and content_sha256 != page_hashes[path]:
            raise ValueError("selected catalog page changed during verification")
        files.append({"path": path.relative_to(site).as_posix(), "bytes": len(content), "sha256": content_sha256})
    digest = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"schema": 1, "scope": "catalog authored article destinations and anchors only", "site_url": site_url, "pages": len(pages), "references": references, "errors": errors, "passed": not errors, "bundle_sha256": digest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--site-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    from mkdocs.config import load_config
    config = load_config(config_file=str(args.config))
    report = inspect_catalog(args.site_dir or Path(config.site_dir), config.site_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Catalog article references: {report['references']}; broken destinations: {len(report['errors'])}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
