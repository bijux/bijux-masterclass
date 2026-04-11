from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.docs_nav import build_tree_nav


def on_config(config):
    """Load program navigation directly from the course-book tree."""
    docs_dir = Path(config.docs_dir).resolve()
    if docs_dir.name != "course-book":
        return config

    config.nav = build_tree_nav(docs_dir)
    return config
