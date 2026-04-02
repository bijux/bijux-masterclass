#!/usr/bin/env python3
"""Render the root MkDocs config with a full library navigation tree."""

from __future__ import annotations

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
    return yaml.safe_load(path.read_text(encoding="utf-8"))


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
        family_nav: list[Any] = [entries[0]]

        for program_item in entries[1:]:
            program_name, overview_path = next(iter(program_item.items()))
            program_slug = Path(overview_path).stem
            program_dir = PROGRAMS_DIR / family_slug / program_slug
            program_config = load_yaml(program_dir / "mkdocs.yml")
            course_prefix = f"library/{family_slug}/{program_slug}/course-book"
            family_nav.append(
                {
                    program_name: [
                        {"Program Overview": overview_path},
                        {"Course Book": prefixed_nav(program_config["nav"], course_prefix)},
                        {"Capstone": capstone_nav(program_dir, family_slug, program_slug)},
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
