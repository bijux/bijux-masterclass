#!/usr/bin/env python3
"""Check the rendered masterclass navigation contract."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_DIR = REPO_ROOT / "artifacts" / "site" / "bijux-masterclass"
COURSE_ROW_LABELS = (
    "Home",
    "Guides",
    "M01",
    "M02",
    "M03",
    "M04",
    "M05",
    "M06",
    "M07",
    "M08",
    "M09",
    "M10",
    "Capstone",
    "Reference",
)


@dataclass(frozen=True)
class PageCheck:
    path: str
    course_title: str
    current_label: str
    sidebar_labels: tuple[str, ...] = ()


PAGE_CHECKS = (
    PageCheck(
        path="python-programming/python-functional-programming/index.html",
        course_title="Python Functional Programming",
        current_label="Home",
        sidebar_labels=("Guides", "M01", "Capstone", "Reference"),
    ),
    PageCheck(
        path=(
            "library/python-programming/python-functional-programming/course-book/"
            "module-04-streaming-resilience-failure-handling/"
            "structural-recursion-and-iteration/index.html"
        ),
        course_title="Python Functional Programming",
        current_label="M04",
        sidebar_labels=(
            "Folds and Reductions",
            "Memoization",
            "Refactoring Guide",
        ),
    ),
    PageCheck(
        path=(
            "library/reproducible-research/deep-dive-snakemake/course-book/"
            "module-04-scaling-workflows-interface-boundaries/index.html"
        ),
        course_title="Deep Dive Snakemake",
        current_label="M04",
        sidebar_labels=(
            "Scaling Workflows and Interface Boundaries",
            "Workflow Modularization",
        ),
    ),
)


def fail(message: str) -> None:
    raise AssertionError(message)


def read_page(site_dir: Path, page: PageCheck) -> str:
    path = site_dir / page.path
    if not path.exists():
        fail(f"missing rendered page: {path.relative_to(site_dir)}")
    return path.read_text(encoding="utf-8")


def visible_row_tag(html: str, row: str, title: str | None = None) -> str:
    title_pattern = ""
    if title:
        title_pattern = rf'(?=[^>]*data-bijux-course-title="{re.escape(title)}")'
    matches = re.findall(
        rf'<nav\b(?=[^>]*data-bijux-nav-row="{row}"){title_pattern}[^>]*>',
        html,
    )
    if not matches:
        fail(f"missing {row} navigation row")
    for tag in matches:
        if " hidden" not in tag:
            return tag
    fail(f"{row} navigation row is hidden")


def require_text(html: str, text: str, context: str) -> None:
    if text not in html:
        fail(f"missing {context}: {text}")


def check_course_row(html: str, page: PageCheck) -> None:
    visible_row_tag(html, "site")
    visible_row_tag(html, "program")
    visible_row_tag(html, "course", page.course_title)
    for label in COURSE_ROW_LABELS:
        require_text(html, f">{label}</a>", f"course row label for {page.course_title}")
    require_text(
        html,
        f'aria-current="page">{page.current_label}</a>',
        f"current course row label for {page.course_title}",
    )


def check_sidebar(html: str, page: PageCheck) -> None:
    require_text(
        html,
        'bijux-nav--scoped" aria-label="Navigation" data-bijux-nav-empty="false"',
        f"scoped sidebar for {page.path}",
    )
    for label in page.sidebar_labels:
        require_text(html, label, f"sidebar label for {page.path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=DEFAULT_SITE_DIR,
        help="Rendered MkDocs site directory to inspect.",
    )
    args = parser.parse_args()

    for page in PAGE_CHECKS:
        html = read_page(args.site_dir, page)
        check_course_row(html, page)
        check_sidebar(html, page)

    print(f"navigation checks passed for {len(PAGE_CHECKS)} rendered pages")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
