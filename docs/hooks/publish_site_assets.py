from __future__ import annotations

import shutil
from pathlib import Path


ROOT_ICON_FILENAMES = (
    "favicon.ico",
    "apple-touch-icon.png",
    "apple-touch-icon-precomposed.png",
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SHARED_ICON_SOURCE_DIR = REPO_ROOT / "docs" / "assets" / "site-icons"


def _icon_source_dir(config) -> Path:
    docs_dir = Path(config.docs_dir)
    course_icon_dir = docs_dir / "assets" / "site-icons"
    if course_icon_dir.exists():
        return course_icon_dir
    return SHARED_ICON_SOURCE_DIR


def on_post_build(config) -> None:
    """Publish browser-probed site icons into the built site root."""
    site_dir = Path(config.site_dir)
    icon_source_dir = _icon_source_dir(config)

    for filename in ROOT_ICON_FILENAMES:
        source_path = icon_source_dir / filename
        if not source_path.exists():
            raise FileNotFoundError(f"Missing site icon source: {source_path}")
        destination_path = site_dir / filename
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
