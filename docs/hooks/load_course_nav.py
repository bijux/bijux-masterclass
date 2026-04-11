from __future__ import annotations

import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.docs_nav import explicit_course_nav
from scripts.sync_series_docs import sync_program_docs


PROGRAMS_ROOT = REPO_ROOT / "programs"
STAGED_PROGRAM_DOCS_ROOT = REPO_ROOT / "artifacts" / "program-docs"


def on_config(config):
    """Load program navigation from the staged public program docs tree."""
    docs_dir = Path(config.docs_dir).resolve()
    if docs_dir.name != "course-book":
        return config

    program_root = docs_dir.parent
    program_slug = program_root.relative_to(PROGRAMS_ROOT)
    staged_docs_dir = STAGED_PROGRAM_DOCS_ROOT / program_slug
    if staged_docs_dir.exists():
        shutil.rmtree(staged_docs_dir)
    sync_program_docs(program_root, staged_docs_dir)

    config.docs_dir = str(staged_docs_dir)
    explicit_nav = explicit_course_nav(program_root)
    if explicit_nav is None:
        raise ValueError(f"missing explicit course nav in {program_root / 'mkdocs.yml'}")
    config.nav = explicit_nav
    return config
