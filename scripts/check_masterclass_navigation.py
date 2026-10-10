#!/usr/bin/env python3
"""Verify authored course order and the complete rendered catalog navigation."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_DIR = REPO_ROOT / "artifacts" / "site" / "bijux-masterclass"
PROGRAMS_ROOT = REPO_ROOT / "programs"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
REPRESENTATIVE_PAGES = (
    'reproducible-research/index.html',
    'reproducible-research/deep-dive-make/index.html',
    'reproducible-research/deep-dive-make/module-01-build-graph-foundations-truth/index.html',
    'reproducible-research/deep-dive-make/module-02-parallel-safety-project-structure/index.html',
    'reproducible-research/deep-dive-make/module-03-determinism-debugging-self-testing/index.html',
    'reproducible-research/deep-dive-make/capstone-docs/index.html',
    'python-programming/index.html',
    'python-programming/python-functional-programming/index.html',
    'python-programming/python-functional-programming/module-04-streaming-resilience-failure-handling/structural-recursion-and-iteration/index.html',
    'reproducible-research/deep-dive-snakemake/module-04-scaling-workflows-interface-boundaries/index.html',
)


def fail(message: str) -> None:
    raise AssertionError(message)


class CatalogNavigation(HTMLParser):
    """Read native tree entries without counting desktop rows or registry links."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_navigation = False
        self.complete = False
        self.entries: list[tuple[str, str, str | None, bool]] = []
        self.capture: tuple[str, str | None, bool] | None = None
        self.label: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "nav" and attributes.get("id") == "bijux-navigation":
            self.in_navigation = True
            self.complete = attributes.get("data-bijux-nav-variant") == "complete"
        if not self.in_navigation:
            return
        if tag == "summary" or (
            tag == "a" and "md-nav__link" in (attributes.get("class") or "").split()
        ):
            self.capture = (
                tag,
                attributes.get("href"),
                attributes.get("aria-current") == "page",
            )
            self.label = []

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.label.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.capture and tag == self.capture[0]:
            kind, href, current = self.capture
            self.entries.append((kind, " ".join("".join(self.label).split()), href, current))
            self.capture = None
        if tag == "nav":
            self.in_navigation = False


def authored_entries(nav: list[dict]) -> list[tuple[str, str, str | None]]:
    entries = []
    for item in nav:
        for label, target in item.items():
            if isinstance(target, list):
                entries.append(("summary", label, None))
                entries.extend(authored_entries(target))
            else:
                path = Path(target)
                url = str(path.with_suffix(""))
                if path.name == "index.md":
                    url = str(path.parent)
                destination = "/" if url == "." else "/" + url + "/"
                entries.append(("a", label, destination))
    return entries


def check_rendered_navigation(html: str, page: str, expected: list[tuple[str, str, str | None]]) -> None:
    navigation = CatalogNavigation()
    navigation.feed(html)
    if not navigation.complete:
        fail(f"missing complete catalog navigation for {page}")
    actual = []
    current = []
    for kind, label, href, active in navigation.entries:
        destination = (
            unquote(urlsplit(urljoin("https://docs.invalid/" + page, href)).path)
            if href is not None else None
        )
        actual.append((kind, label, destination))
        if active:
            current.append(destination)
    if actual != expected:
        mismatch = next(
            (index for index, pair in enumerate(zip(actual, expected)) if pair[0] != pair[1]),
            min(len(actual), len(expected)),
        )
        fail(
            f"catalog navigation differs from authored order for {page} at entry {mismatch}: "
            f"{actual[mismatch:mismatch+1]} != {expected[mismatch:mismatch+1]}"
        )
    current_path = "/" + page.removesuffix("index.html")
    if not current or any(destination != current_path for destination in current):
        fail(f"current-page navigation does not identify {page}: {current}")


def same_directory_link_targets(index_path: Path) -> set[str]:
    linked_names: set[str] = set()
    directory = index_path.parent
    for match in MARKDOWN_LINK_RE.finditer(index_path.read_text(encoding="utf-8")):
        target = match.group(1).strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = Path(target)
        if target_path.is_absolute():
            continue

        parts = [part for part in target_path.parts if part != "."]
        if not parts or parts[0] == "..":
            continue

        candidate = (directory / target_path).resolve()
        if (
            candidate.exists()
            and candidate.is_file()
            and candidate.parent == directory.resolve()
            and candidate.suffix == ".md"
            and candidate.name != "index.md"
        ):
            linked_names.add(candidate.name)
    return linked_names


def check_authored_source_navigation(programs_root: Path) -> int:
    checked_directories = 0
    failures: list[str] = []
    for index_path in sorted(programs_root.glob("**/index.md")):
        directory = index_path.parent
        md_files = sorted(
            path.name
            for path in directory.glob("*.md")
            if path.name != "index.md"
        )
        if not md_files:
            continue

        checked_directories += 1
        linked_names = same_directory_link_targets(index_path)
        missing = [name for name in md_files if name not in linked_names]
        if missing:
            failures.append(
                f"{directory.relative_to(REPO_ROOT)} missing authored order for: {', '.join(missing)}"
            )

    if failures:
        fail("\n".join(failures))
    return checked_directories


def check_explicit_course_navigation(programs_root: Path) -> int:
    import yaml

    sys.path.insert(0, str(REPO_ROOT))
    from scripts.docs_nav import build_tree_nav

    checked_courses = 0
    failures: list[str] = []
    for config_path in sorted(programs_root.glob("**/mkdocs.yml")):
        checked_courses += 1
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        nav = config.get("nav")
        if nav is None:
            failures.append(f"{config_path.relative_to(REPO_ROOT)} is missing explicit nav")
            continue
        expected = build_tree_nav(config_path.parent / "course-book")
        if nav != expected:
            failures.append(
                f"{config_path.relative_to(REPO_ROOT)} nav does not match authored course order"
            )

    if failures:
        fail("\n".join(failures))
    return checked_courses


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=DEFAULT_SITE_DIR)
    args = parser.parse_args()
    checked_courses = check_explicit_course_navigation(PROGRAMS_ROOT)
    checked_directories = check_authored_source_navigation(PROGRAMS_ROOT)
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.render_root_mkdocs import SOURCE_CONFIG, load_yaml, root_nav

    expected = authored_entries(root_nav(load_yaml(SOURCE_CONFIG)["nav"]))
    for page in REPRESENTATIVE_PAGES:
        path = args.site_dir / page
        if not path.is_file():
            fail(f"missing rendered page: {page}")
        check_rendered_navigation(path.read_text(encoding="utf-8"), page, expected)
    print(f"navigation checks passed for {checked_courses} course configs, "
          f"{checked_directories} source directories, {len(expected)} catalog entries "
          f"and {len(REPRESENTATIVE_PAGES)} rendered pages")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
