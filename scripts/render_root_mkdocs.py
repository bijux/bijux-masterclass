#!/usr/bin/env python3
"""Render the root MkDocs config with a full library navigation tree."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CONFIG = REPO_ROOT / "mkdocs.yml"
PROGRAMS_DIR = REPO_ROOT / "programs"
OUTPUT_CONFIG = REPO_ROOT / "artifacts" / "mkdocs.root.yml"

CAPSTONE_ORDER = {
    "README": 0,
    "ARCHITECTURE": 1,
    "PACKAGE_GUIDE": 2,
    "TEST_GUIDE": 3,
    "WALKTHROUGH_GUIDE": 4,
    "TARGET_GUIDE": 5,
    "INSPECTION_GUIDE": 6,
    "EXTENSION_GUIDE": 7,
    "EXPERIMENT_GUIDE": 8,
    "RECOVERY_GUIDE": 9,
    "RELEASE_REVIEW_GUIDE": 10,
    "PUBLISH_REVIEW_GUIDE": 11,
    "PUBLISH_CONTRACT": 12,
    "FILE_API": 13,
    "CONTRACT_AUDIT_GUIDE": 14,
    "INCIDENT_REVIEW_GUIDE": 15,
    "PROFILE_AUDIT_GUIDE": 16,
    "REPRO_GUIDE": 17,
    "SELFTEST_GUIDE": 18,
    "PROOF_GUIDE": 19,
    "TOUR": 20,
}


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


def prefixed_nav(items: list[Any], prefix: str) -> list[Any]:
    prefixed: list[Any] = []
    for item in items:
        if isinstance(item, dict):
            key, value = next(iter(item.items()))
            if isinstance(value, str):
                prefixed.append({key: f"{prefix}/{value}"})
            elif isinstance(value, list):
                prefixed.append({key: prefixed_nav(value, prefix)})
            else:
                raise TypeError(f"Unsupported nav value type for {key!r}: {type(value)!r}")
        else:
            raise TypeError(f"Unsupported nav item type: {type(item)!r}")
    return prefixed


def nav_entry(item: Any) -> tuple[str, Any]:
    if not isinstance(item, dict):
        raise TypeError(f"Unsupported nav item type: {type(item)!r}")
    return next(iter(item.items()))


def as_nav_list(title: str, value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [{title: value}]
    raise TypeError(f"Unsupported nav value type for {title!r}: {type(value)!r}")


def module_label(title: str) -> str:
    match = re.search(r"\bModule\s+(\d+)\b", title)
    if not match:
        return title
    return f"M{int(match.group(1)):02d}"


def course_book_nav(
    items: list[Any],
    prefix: str,
    project_capstone_nav: list[Any],
) -> list[Any]:
    prefixed = prefixed_nav(items, prefix)
    sections: dict[str, Any] = {}
    modules: list[Any] = []
    uncategorized: list[Any] = []

    for item in prefixed:
        key, value = nav_entry(item)
        if key == "Modules":
            modules = as_nav_list(key, value)
        elif key in {"Start Here", "Guides", "Reference", "Capstone"}:
            sections[key] = value
        else:
            uncategorized.append({key: value})

    guides: list[Any] = []
    for section_name in ("Start Here", "Guides"):
        if section_name in sections:
            guides.extend(as_nav_list(section_name, sections[section_name]))
    guides.extend(uncategorized)

    module_nav: list[Any] = []
    capstone_extras: list[Any] = []
    for item in modules:
        key, value = nav_entry(item)
        label = module_label(key)
        if label == key:
            if "capstone" in key.lower():
                capstone_extras.append({key: value})
            elif module_nav:
                previous_key, previous_value = nav_entry(module_nav[-1])
                if isinstance(previous_value, list):
                    previous_value.append({key: value})
                else:
                    module_nav[-1] = {
                        previous_key: [{previous_key: previous_value}, {key: value}]
                    }
            else:
                guides.append({key: value})
        else:
            module_nav.append({label: value})

    nav: list[Any] = []
    if guides:
        nav.append({"Guides": guides})
    nav.extend(module_nav)

    capstone: list[Any] = []
    course_book_capstone: list[Any] = []
    if "Capstone" in sections:
        course_book_capstone.extend(as_nav_list("Capstone", sections["Capstone"]))
    course_book_capstone.extend(capstone_extras)
    if course_book_capstone:
        capstone.append({"Course Book": course_book_capstone})
    if project_capstone_nav:
        capstone.append({"Project Docs": project_capstone_nav})
    if capstone:
        nav.append({"Capstone": capstone})

    if "Reference" in sections:
        nav.append({"Reference": as_nav_list("Reference", sections["Reference"])})

    return nav


def capstone_nav(program_dir: Path, family_slug: str, program_slug: str) -> list[Any]:
    capstone_dir = program_dir / "capstone"
    readme_path = capstone_dir / "README.md"
    docs_dir = capstone_dir / "docs"
    docs_files = sorted(
        docs_dir.glob("*.md"),
        key=lambda path: (CAPSTONE_ORDER.get(path.stem, 999), path.stem),
    )

    nav: list[Any] = []
    if readme_path.exists():
        nav.append(
            {
                first_h1(readme_path): f"library/{family_slug}/{program_slug}/capstone/{readme_path.name}",
            }
        )
    if docs_files:
        nav.append(
            {
                "Capstone Docs": [
                    {
                        first_h1(path): f"library/{family_slug}/{program_slug}/capstone/docs/{path.name}",
                    }
                    for path in docs_files
                ]
            }
        )

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
            program_dir = PROGRAMS_DIR / family_slug / program_slug
            program_config = load_yaml(program_dir / "mkdocs.yml")
            course_prefix = f"library/{family_slug}/{program_slug}/course-book"
            project_capstone_nav = capstone_nav(program_dir, family_slug, program_slug)
            family_nav.append(
                {
                    program_name: [
                        {"Home": overview_path},
                        *course_book_nav(
                            program_config["nav"],
                            course_prefix,
                            project_capstone_nav,
                        ),
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
