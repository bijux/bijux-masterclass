#!/usr/bin/env python3
"""Check the rendered masterclass navigation contract."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_DIR = REPO_ROOT / "artifacts" / "site" / "bijux-masterclass"
PROGRAMS_ROOT = REPO_ROOT / "programs"
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
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class PageCheck:
    path: str
    current_label: str
    program_labels: tuple[str, ...]
    course_title: str | None = None
    sidebar_visible: bool = True
    sidebar_labels: tuple[str, ...] = ()
    sidebar_ordered_labels: tuple[str, ...] = ()
    sidebar_absent_labels: tuple[str, ...] = ()


PAGE_CHECKS = (
    PageCheck(
        path="reproducible-research/index.html",
        current_label="Home",
        program_labels=("Home", "Deep Dive Make", "Deep Dive Snakemake", "Deep Dive DVC"),
        sidebar_visible=False,
    ),
    PageCheck(
        path="reproducible-research/deep-dive-make/index.html",
        current_label="Home",
        program_labels=("Home", "Deep Dive Make", "Deep Dive Snakemake", "Deep Dive DVC"),
        course_title="Deep Dive Make",
        sidebar_visible=False,
        sidebar_absent_labels=("Guides", "Guides Home", "Start Here", "M01", "Capstone", "Reference"),
    ),
    PageCheck(
        path=(
            "reproducible-research/deep-dive-make/"
            "module-01-build-graph-foundations-truth/index.html"
        ),
        current_label="M01",
        program_labels=("Home", "Deep Dive Make", "Deep Dive Snakemake", "Deep Dive DVC"),
        course_title="Deep Dive Make",
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
        sidebar_ordered_labels=(
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
            "reproducible-research/deep-dive-make/"
            "module-02-parallel-safety-project-structure/index.html"
        ),
        current_label="M02",
        program_labels=("Home", "Deep Dive Make", "Deep Dive Snakemake", "Deep Dive DVC"),
        course_title="Deep Dive Make",
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
        sidebar_ordered_labels=(
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
            "reproducible-research/deep-dive-make/"
            "module-03-determinism-debugging-self-testing/index.html"
        ),
        current_label="M03",
        program_labels=("Home", "Deep Dive Make", "Deep Dive Snakemake", "Deep Dive DVC"),
        course_title="Deep Dive Make",
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
        sidebar_ordered_labels=(
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
            "reproducible-research/deep-dive-make/"
            "capstone-docs/index.html"
        ),
        current_label="Capstone Docs",
        program_labels=("Home", "Deep Dive Make", "Deep Dive Snakemake", "Deep Dive DVC"),
        course_title="Deep Dive Make",
        sidebar_labels=("Home", "Architecture Guide", "Proof Guide"),
        sidebar_absent_labels=("Reference", "M01"),
    ),
    PageCheck(
        path="python-programming/index.html",
        current_label="Home",
        program_labels=(
            "Home",
            "Python Object-Oriented Programming",
            "Python Functional Programming",
            "Python Metaprogramming",
        ),
        sidebar_visible=False,
    ),
    PageCheck(
        path="python-programming/python-functional-programming/index.html",
        current_label="Home",
        program_labels=(
            "Home",
            "Python Object-Oriented Programming",
            "Python Functional Programming",
            "Python Metaprogramming",
        ),
        course_title="Python Functional Programming",
        sidebar_visible=False,
        sidebar_absent_labels=("Guides", "M01", "Capstone", "Capstone Docs", "Reference"),
    ),
    PageCheck(
        path=(
            "python-programming/python-functional-programming/"
            "module-04-streaming-resilience-failure-handling/"
            "structural-recursion-and-iteration/index.html"
        ),
        current_label="M04",
        program_labels=(
            "Home",
            "Python Object-Oriented Programming",
            "Python Functional Programming",
            "Python Metaprogramming",
        ),
        course_title="Python Functional Programming",
        sidebar_labels=(
            "Folds and Reductions",
            "Memoization",
            "Refactoring Guide",
        ),
        sidebar_ordered_labels=(
            "Structural Recursion and Iteration",
            "Folds and Reductions",
            "Memoization",
            "Result and Option Failures",
            "Streaming Error Handling",
            "Error Aggregation",
            "Circuit Breakers",
            "Resource-Aware Streams",
            "Functional Retries",
            "Structured Error Reports",
            "Module 04 Refactoring Guide",
            "Module Glossary",
        ),
    ),
    PageCheck(
        path=(
            "reproducible-research/deep-dive-snakemake/"
            "module-04-scaling-workflows-interface-boundaries/index.html"
        ),
        current_label="M04",
        program_labels=("Home", "Deep Dive Make", "Deep Dive Snakemake", "Deep Dive DVC"),
        course_title="Deep Dive Snakemake",
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


def row_html(html: str, row: str, title: str | None = None) -> str:
    title_pattern = ""
    if title:
        title_pattern = rf'(?=[^>]*data-bijux-course-title="{re.escape(title)}")'
    matches = re.findall(
        rf'<nav\b(?=[^>]*data-bijux-nav-row="{row}"){title_pattern}[^>]*>.*?</nav>',
        html,
        flags=re.DOTALL,
    )
    if not matches:
        fail(f"missing {row} navigation row")
    for match in matches:
        tag = match.split(">", 1)[0]
        if " hidden" not in tag:
            return match
    fail(f"{row} navigation row is hidden")


def require_text(html: str, text: str, context: str) -> None:
    if text not in html:
        fail(f"missing {context}: {text}")


def forbid_text(html: str, text: str, context: str) -> None:
    if text in html:
        fail(f"unexpected {context}: {text}")


def require_ordered_text(html: str, texts: tuple[str, ...], context: str) -> None:
    cursor = -1
    for text in texts:
        position = html.find(text, cursor + 1)
        if position == -1:
            fail(f"missing ordered {context}: {text}")
        if position < cursor:
            fail(f"out-of-order {context}: {text}")
        cursor = position


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
    program_html = row_html(html, "program")
    for label in page.program_labels:
        if not re.search(rf">\s*{re.escape(label)}\s*</a>", program_html):
            fail(f"missing program row label for {page.path}: {label}")
    if page.course_title is None:
        visible_course_rows = [
            tag
            for tag in re.findall(r'<nav\b(?=[^>]*data-bijux-nav-row="course")[^>]*>', html)
            if " hidden" not in tag
        ]
        if visible_course_rows:
            fail(f"unexpected course navigation row for {page.path}")
    else:
        course_html = row_html(html, "course", page.course_title)
        for label in COURSE_ROW_LABELS:
            if not re.search(rf">\s*{re.escape(label)}\s*</a>", course_html):
                fail(f"missing course row label for {page.course_title}: {label}")
    if not re.search(
        rf'aria-current="page">\s*{re.escape(page.current_label)}\s*</a>',
        html,
    ):
        fail(f"missing current course row label for {page.course_title}: {page.current_label}")


def check_sidebar(html: str, page: PageCheck) -> None:
    sidebar_html = scoped_sidebar_html(html, page)
    expected_empty = "false" if page.sidebar_visible else "true"
    require_text(
        sidebar_html,
        f'bijux-nav--scoped" aria-label="Navigation" data-bijux-nav-empty="{expected_empty}"',
        f"scoped sidebar for {page.path}",
    )
    if not page.sidebar_visible:
        return
    for label in page.sidebar_labels:
        require_text(sidebar_html, label, f"sidebar label for {page.path}")
    if page.sidebar_ordered_labels:
        require_ordered_text(
            sidebar_html,
            page.sidebar_ordered_labels,
            f"sidebar label order for {page.path}",
        )
    for label in page.sidebar_absent_labels:
        forbid_text(sidebar_html, label, f"sidebar label for {page.path}")


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
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=DEFAULT_SITE_DIR,
        help="Rendered MkDocs site directory to inspect.",
    )
    args = parser.parse_args()

    checked_courses = check_explicit_course_navigation(PROGRAMS_ROOT)
    checked_directories = check_authored_source_navigation(PROGRAMS_ROOT)
    for page in PAGE_CHECKS:
        html = read_page(args.site_dir, page)
        check_course_row(html, page)
        check_sidebar(html, page)

    print(
        "navigation checks passed for "
        f"{checked_courses} course configs, {checked_directories} source directories, "
        f"and {len(PAGE_CHECKS)} rendered pages"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
