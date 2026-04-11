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
    "M00",
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
    "Capstone Docs",
    "Reference",
)


@dataclass(frozen=True)
class PageCheck:
    path: str
    course_title: str
    current_label: str
    sidebar_labels: tuple[str, ...] = ()
    sidebar_absent_labels: tuple[str, ...] = ()


PAGE_CHECKS = (
    PageCheck(
        path="reproducible-research/deep-dive-make/index.html",
        course_title="Deep Dive Make",
        current_label="Home",
        sidebar_labels=("Home",),
        sidebar_absent_labels=("Guides", "Guides Home", "Start Here", "M01", "Capstone", "Reference"),
    ),
    PageCheck(
        path=(
            "library/reproducible-research/deep-dive-make/"
            "module-01-build-graph-foundations-truth/index.html"
        ),
        course_title="Deep Dive Make",
        current_label="M01",
        sidebar_labels=(
            "Home",
            "Build Graph Mental Model",
            "Rebuild Truth and Convergence",
            "Rule Shapes and Target Ownership",
            "Evaluation and Expansion",
            "Atomic Publication and Dependency Tracking",
            "Worked Example: Tiny C Build",
            "Exercises",
            "Exercise Answers",
            "Glossary",
        ),
        sidebar_absent_labels=("Capstone", "Capstone Docs", "Reference", "M02"),
    ),
    PageCheck(
        path=(
            "library/reproducible-research/deep-dive-make/"
            "module-02-parallel-safety-project-structure/index.html"
        ),
        course_title="Deep Dive Make",
        current_label="M02",
        sidebar_labels=(
            "Home",
            "Parallel Scheduling and Runnable Targets",
            "Parallel Safety Contract",
            "Ordering Tools and Honest Edges",
            "Project Structure with One DAG",
            "Selftests and Race Repro Pack",
            "Worked Example: Parallel-Safe Build",
            "Exercises",
            "Exercise Answers",
            "Glossary",
        ),
        sidebar_absent_labels=("Capstone", "Capstone Docs", "Reference", "M03"),
    ),
    PageCheck(
        path=(
            "library/reproducible-research/deep-dive-make/"
            "module-03-determinism-debugging-self-testing/index.html"
        ),
        course_title="Deep Dive Make",
        current_label="M03",
        sidebar_labels=(
            "Home",
            "Determinism and Stable Discovery",
            "Forensic Debugging with Make Evidence",
            "CI Targets as a Public Contract",
            "Build-System Selftests",
            "Macros and Quarantined Eval",
            "Worked Example: Production Simulator",
            "Exercises",
            "Exercise Answers",
            "Glossary",
        ),
        sidebar_absent_labels=("Capstone", "Capstone Docs", "Reference", "M04"),
    ),
    PageCheck(
        path=(
            "library/reproducible-research/deep-dive-make/"
            "capstone-docs/index.html"
        ),
        course_title="Deep Dive Make",
        current_label="Capstone Docs",
        sidebar_labels=("Home", "Architecture Guide", "Proof Guide"),
        sidebar_absent_labels=("Reference", "M01"),
    ),
    PageCheck(
        path="python-programming/python-functional-programming/index.html",
        course_title="Python Functional Programming",
        current_label="Home",
        sidebar_labels=("Home",),
        sidebar_absent_labels=("Guides", "M01", "Capstone", "Capstone Docs", "Reference"),
    ),
    PageCheck(
        path=(
            "library/python-programming/python-functional-programming/"
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
            "library/reproducible-research/deep-dive-snakemake/"
            "module-04-scaling-workflows-interface-boundaries/index.html"
        ),
        course_title="Deep Dive Snakemake",
        current_label="M04",
        sidebar_labels=("Home", "Glossary"),
        sidebar_absent_labels=("Capstone", "Capstone Docs", "Reference", "M05"),
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


def forbid_text(html: str, text: str, context: str) -> None:
    if text in html:
        fail(f"unexpected {context}: {text}")


def scoped_sidebar_html(html: str, page: PageCheck) -> str:
    marker = 'bijux-nav--scoped" aria-label="Navigation"'
    start = html.find(marker)
    if start == -1:
        fail(f"missing scoped sidebar for {page.path}")
    end = html.find('md-sidebar--secondary', start)
    if end == -1:
        return html[start:]
    return html[start:end]


def check_course_row(html: str, page: PageCheck) -> None:
    visible_row_tag(html, "site")
    visible_row_tag(html, "program")
    visible_row_tag(html, "course", page.course_title)
    for label in COURSE_ROW_LABELS:
        if not re.search(rf">\s*{re.escape(label)}\s*</a>", html):
            fail(f"missing course row label for {page.course_title}: {label}")
    if not re.search(
        rf'aria-current="page">\s*{re.escape(page.current_label)}\s*</a>',
        html,
    ):
        fail(f"missing current course row label for {page.course_title}: {page.current_label}")


def check_sidebar(html: str, page: PageCheck) -> None:
    sidebar_html = scoped_sidebar_html(html, page)
    require_text(
        sidebar_html,
        'bijux-nav--scoped" aria-label="Navigation" data-bijux-nav-empty="false"',
        f"scoped sidebar for {page.path}",
    )
    for label in page.sidebar_labels:
        require_text(sidebar_html, label, f"sidebar label for {page.path}")
    for label in page.sidebar_absent_labels:
        forbid_text(sidebar_html, label, f"sidebar label for {page.path}")


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
