#!/usr/bin/env python3
"""Shared navigation builders for course-book and catalog docs."""

from __future__ import annotations

from functools import lru_cache
import re
from pathlib import Path
from typing import Any


CAPSTONE_DOCS_DIRNAMES = {"capstone-docs"}
MODULE_DIR_PATTERN = re.compile(r"module-(\d+)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def first_h1(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def humanize_dirname(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def module_number(name: str) -> int | None:
    match = MODULE_DIR_PATTERN.match(name)
    if match is None:
        return None
    return int(match.group(1))


def directory_sort_key(path: Path) -> tuple[int, int, str]:
    name = path.name
    number = module_number(name)
    if name == "guides":
        return (0, -1, name)
    if number is not None:
        return (1, number, name)
    if name == "capstone":
        return (2, -1, name)
    if name in CAPSTONE_DOCS_DIRNAMES:
        return (3, -1, name)
    if name == "reference":
        return (4, -1, name)
    return (5, -1, name)


def normalize_link_target(target: str) -> str:
    target = target.strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return ""
    return target.split("#", 1)[0]


def uses_structural_directory_order(directory: Path) -> bool:
    return any(
        child.is_dir() and (
            child.name == "guides"
            or child.name == "reference"
            or child.name == "capstone"
            or child.name in CAPSTONE_DOCS_DIRNAMES
            or module_number(child.name) is not None
        )
        for child in directory.iterdir()
    )


@lru_cache(maxsize=None)
def index_child_order(directory: Path) -> dict[str, int]:
    index_path = directory / "index.md"
    if not index_path.exists():
        return {}

    structural_directory_order = uses_structural_directory_order(directory)
    order: dict[str, int] = {}
    for match in MARKDOWN_LINK_RE.finditer(index_path.read_text(encoding="utf-8")):
        target = normalize_link_target(match.group(1))
        if not target:
            continue

        target_path = Path(target)
        if target_path.is_absolute():
            continue

        parts = [part for part in target_path.parts if part not in (".",)]
        if not parts or parts[0] == "..":
            continue

        child_name = parts[0]
        child_path = directory / child_name

        if child_name == "index.md" or not child_path.exists():
            continue
        if structural_directory_order and child_path.is_dir():
            continue
        order.setdefault(child_name, len(order))

    return order


def child_sort_key(path: Path, sibling_order: dict[str, int]) -> tuple[int, int, int, int, str]:
    explicit_position = sibling_order.get(path.name, 10_000)
    if path.name == "index.md":
        return (0, explicit_position, -1, -1, path.name)
    if path.is_dir():
        group, number, name = directory_sort_key(path)
        return (1, explicit_position, group, number, name)
    return (2, explicit_position, -1, -1, path.name)


def directory_title(path: Path) -> str:
    if path.name in CAPSTONE_DOCS_DIRNAMES:
        return "Capstone Docs"

    index_path = path / "index.md"
    if index_path.exists():
        return first_h1(index_path)
    return humanize_dirname(path.name)


def nav_path(prefix: str, name: str) -> str:
    return f"{prefix}/{name}" if prefix else name


def build_tree_nav(
    directory: Path,
    prefix: str = "",
    *,
    include_root_home: bool = True,
) -> list[Any]:
    nav: list[Any] = []
    sibling_order = index_child_order(directory)

    index_path = directory / "index.md"
    if include_root_home and index_path.exists():
        nav.append({"Home": nav_path(prefix, "index.md")})

    for child in sorted(directory.iterdir(), key=lambda path: child_sort_key(path, sibling_order)):
        if child.name == "index.md":
            continue
        if child.is_file() and child.suffix == ".md":
            nav.append({first_h1(child): nav_path(prefix, child.name)})
            continue
        if child.is_dir():
            child_nav = build_tree_nav(child, nav_path(prefix, child.name))
            if child_nav:
                nav.append({directory_title(child): child_nav})

    return nav
