#!/usr/bin/env python3
"""Render the root MkDocs config from the synced library tree."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.docs_nav import build_tree_nav

SOURCE_CONFIG = REPO_ROOT / "mkdocs.yml"
LIBRARY_ROOT = REPO_ROOT / "docs" / "library"
OUTPUT_CONFIG = REPO_ROOT / "artifacts" / "mkdocs.root.yml"


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


def root_nav(source_nav: list[Any]) -> list[Any]:
    generated: list[Any] = [source_nav[0]]

    for family_item in source_nav[1:]:
        family_name, family_home = next(iter(family_item.items()))
        family_slug = Path(family_home).parent.name
        family_root = LIBRARY_ROOT / family_slug
        generated.append(
            {
                family_name: build_tree_nav(
                    family_root,
                    f"library/{family_slug}",
                )
            }
        )

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
