#!/usr/bin/env python3
"""Sync explicit MkDocs navigation for masterclass courses."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import re
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.docs_nav import build_tree_nav


def course_configs(paths: list[Path]) -> list[Path]:
    if paths:
        return [path.resolve() for path in paths]
    return sorted((REPO_ROOT / "programs").glob("**/mkdocs.yml"))


TOP_LEVEL_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:")


def nav_block_text(nav: list[Any]) -> str:
    rendered = yaml.safe_dump(
        {"nav": nav},
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    )
    return rendered.rstrip() + "\n"


def strip_existing_nav_block(text: str) -> str:
    lines = text.splitlines(keepends=True)
    stripped: list[str] = []
    inside_nav = False
    for line in lines:
        if not inside_nav and line.startswith("nav:"):
            inside_nav = True
            continue
        if inside_nav and TOP_LEVEL_KEY_RE.match(line):
            inside_nav = False
        if not inside_nav:
            stripped.append(line)
    return "".join(stripped)


def rendered_config_text(path: Path) -> str:
    nav = build_tree_nav(path.parent / "course-book")
    nav_text = nav_block_text(nav)
    current = strip_existing_nav_block(path.read_text(encoding="utf-8"))
    site_dir_match = re.search(r"^site_dir:.*\n", current, re.MULTILINE)
    if site_dir_match is None:
        raise AssertionError(f"expected site_dir in {path}")
    return current.replace(site_dir_match.group(0), site_dir_match.group(0) + "\n" + nav_text, 1)


def sync_config(path: Path, *, check: bool) -> bool:
    current = path.read_text(encoding="utf-8")
    rendered = rendered_config_text(path)
    if current == rendered:
        return False
    if check:
        diff = "".join(
            difflib.unified_diff(
                current.splitlines(keepends=True),
                rendered.splitlines(keepends=True),
                fromfile=str(path),
                tofile=f"{path} (expected)",
            )
        )
        raise AssertionError(diff.rstrip())
    path.write_text(rendered, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="MkDocs course config paths to sync. Defaults to every programs/**/mkdocs.yml",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of writing when a config is out of sync.",
    )
    args = parser.parse_args()

    changed = 0
    for path in course_configs(args.paths):
        if sync_config(path, check=args.check):
            changed += 1
            if not args.check:
                print(f"updated {path.relative_to(REPO_ROOT)}")

    if args.check:
        print(f"course nav is synchronized for {len(course_configs(args.paths))} configs")
    else:
        print(f"synchronized {changed} course configs")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
