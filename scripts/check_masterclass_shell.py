#!/usr/bin/env python3
"""Check that the rendered masterclass shell matches the shared site contract."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_DIR = REPO_ROOT / "artifacts" / "site"


def fail(message: str) -> None:
    raise AssertionError(message)


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing rendered page: {path.relative_to(REPO_ROOT)}")
    return path.read_text(encoding="utf-8")


def require_text(html: str, text: str, context: str) -> None:
    if text not in html:
        fail(f"missing {context}: {text}")


def check_palette_contract(page: Path) -> None:
    html = read_text(page)
    require_text(html, 'data-md-color-primary="teal"', f"teal palette on {page.name}")
    require_text(html, 'data-md-color-accent="cyan"', f"cyan accent on {page.name}")
    require_text(html, "Switch to dark mode", f"dark-mode toggle on {page.name}")
    require_text(html, "Switch to light mode", f"light-mode toggle on {page.name}")


def check_shell_assets(page: Path) -> None:
    html = read_text(page)
    require_text(
        html,
        "assets/javascripts/external-links.js",
        f"external-link script on {page.name}",
    )


def check_landing_layout(page: Path) -> None:
    html = read_text(page)
    require_text(html, "bijux-hero", f"hero shell on {page.name}")
    require_text(html, "bijux-panel-grid", f"panel grid on {page.name}")
    require_text(html, "bijux-topic-pill", f"topic pills on {page.name}")


def main(argv: list[str]) -> int:
    site_dir = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_SITE_DIR
    root_page = site_dir / "index.html"
    python_page = site_dir / "python-programming" / "index.html"
    research_page = site_dir / "reproducible-research" / "index.html"
    course_page = site_dir / "python-programming" / "python-functional-programming" / "index.html"

    for page in (root_page, python_page, research_page, course_page):
        check_palette_contract(page)
        check_shell_assets(page)

    for page in (root_page, python_page, research_page):
        check_landing_layout(page)

    print("masterclass shell checks passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
