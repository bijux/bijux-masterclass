#!/usr/bin/env python3
"""Render the root MkDocs config from the synced library tree."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CONFIG = REPO_ROOT / "mkdocs.yml"
LIBRARY_ROOT = REPO_ROOT / "docs" / "library"
OUTPUT_CONFIG = REPO_ROOT / "artifacts" / "mkdocs.root.yml"
PROJECT_DOCS_DIRNAME = "project-docs"


def load_yaml(path: Path) -> dict[str, Any]:
    class EnvSafeLoader(yaml.SafeLoader):
        """Safe YAML loader with minimal support for MkDocs-style !ENV tags."""

    def construct_env_tag(
        loader: EnvSafeLoader,
        node: yaml.ScalarNode | yaml.SequenceNode,
    ) -> str:
        if isinstance(node, yaml.ScalarNode):
            var_name = loader.construct_scalar(node)
            return os.getenv(var_name, "")
        if isinstance(node, yaml.SequenceNode):
            values = loader.construct_sequence(node)
            if not values:
                return ""
            var_name = str(values[0])
            fallback = str(values[1]) if len(values) > 1 else ""
            return os.getenv(var_name, fallback)
        raise TypeError(f"Unsupported !ENV node type: {type(node)!r}")

    EnvSafeLoader.add_constructor("!ENV", construct_env_tag)
    return yaml.load(path.read_text(encoding="utf-8"), Loader=EnvSafeLoader)


def first_h1(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def humanize_dirname(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def directory_sort_key(path: Path) -> tuple[int, str]:
    name = path.name
    if name == "guides":
        return (0, name)
    if name == "reference":
        return (1, name)
    if name == "capstone":
        return (2, name)
    if name.startswith("module-"):
        return (3, name)
    if name == PROJECT_DOCS_DIRNAME:
        return (4, name)
    return (5, name)


def file_sort_key(path: Path) -> tuple[int, str]:
    if path.name == "index.md":
        return (0, path.name)
    return (1, path.name)


def directory_title(path: Path) -> str:
    index_path = path / "index.md"
    if index_path.exists():
        return first_h1(index_path)
    if path.name == PROJECT_DOCS_DIRNAME:
        return "Project Docs"
    return humanize_dirname(path.name)


def tree_nav(directory: Path, prefix: str) -> list[Any]:
    nav: list[Any] = []

    index_path = directory / "index.md"
    if index_path.exists():
        nav.append({"Home": f"{prefix}/index.md"})

    for child in sorted(directory.iterdir(), key=directory_sort_key):
        if child.name == "index.md":
            continue
        if child.is_file() and child.suffix == ".md":
            nav.append({first_h1(child): f"{prefix}/{child.name}"})
            continue
        if child.is_dir():
            child_nav = tree_nav(child, f"{prefix}/{child.name}")
            if child_nav:
                nav.append({directory_title(child): child_nav})

    return nav


def root_nav(source_nav: list[Any]) -> list[Any]:
    generated: list[Any] = [source_nav[0]]

    for family_item in source_nav[1:]:
        family_name, entries = next(iter(family_item.items()))
        family_slug = entries[0]["Overview"].split("/")[0]
        family_nav: list[Any] = [{"Home": entries[0]["Overview"]}]

        for program_item in entries[1:]:
            program_name, overview_path = next(iter(program_item.items()))
            program_slug = Path(overview_path).stem
            program_root = LIBRARY_ROOT / family_slug / program_slug
            course_prefix = f"library/{family_slug}/{program_slug}"
            family_nav.append(
                {
                    program_name: [
                        {"Home": overview_path},
                        *tree_nav(program_root, course_prefix),
                    ]
                }
            )

        generated.append({family_name: family_nav})

    return generated


def main() -> int:
    config = load_yaml(SOURCE_CONFIG)
    config["nav"] = root_nav(config["nav"])
    config["INHERIT"] = "../mkdocs.shared.yml"
    config["docs_dir"] = "../docs"
    config["site_dir"] = "site/bijux-masterclass"
    theme = config.setdefault("theme", {})
    if not isinstance(theme, dict):
        raise TypeError(f"Unsupported theme configuration type: {type(theme)!r}")
    theme["custom_dir"] = "../docs/overrides"
    config["hooks"] = ["../docs/hooks/publish_site_assets.py"]
    OUTPUT_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_CONFIG.write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Rendered root MkDocs config to {OUTPUT_CONFIG.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
