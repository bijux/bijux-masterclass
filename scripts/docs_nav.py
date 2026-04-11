#!/usr/bin/env python3
"""Shared navigation builders for course-book and catalog docs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


CAPSTONE_DOCS_DIRNAMES = {"capstone-docs"}
MODULE_DIR_PATTERN = re.compile(r"module-(\d+)")


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


def child_sort_key(path: Path) -> tuple[int, int, int, str]:
    if path.name == "index.md":
        return (0, -1, -1, path.name)
    if path.is_dir():
        group, number, name = directory_sort_key(path)
        return (1, group, number, name)
    return (2, -1, -1, path.name)


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

    index_path = directory / "index.md"
    if include_root_home and index_path.exists():
        nav.append({"Home": nav_path(prefix, "index.md")})

    for child in sorted(directory.iterdir(), key=child_sort_key):
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
