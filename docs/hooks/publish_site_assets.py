from __future__ import annotations

import shutil
from pathlib import Path


ROOT_ICON_FILENAMES = (
    "favicon.ico",
    "apple-touch-icon.png",
    "apple-touch-icon-precomposed.png",
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SHARED_ASSET_SOURCE_DIR = REPO_ROOT / "docs" / "assets"


def _asset_source_dir(config) -> Path:
    docs_dir = Path(config.docs_dir)
    docs_asset_dir = docs_dir / "assets"
    if docs_asset_dir.exists():
        return docs_asset_dir
    return SHARED_ASSET_SOURCE_DIR


def on_post_build(config) -> None:
    """Publish shared shell assets and browser-probed icons into the built site."""
    site_dir = Path(config.site_dir)
    asset_source_dir = _asset_source_dir(config)
    site_asset_dir = site_dir / "assets"

    if not asset_source_dir.exists():
        raise FileNotFoundError(f"Missing shared site assets: {asset_source_dir}")
    shutil.copytree(asset_source_dir, site_asset_dir, dirs_exist_ok=True)

    for filename in ROOT_ICON_FILENAMES:
        source_path = asset_source_dir / "site-icons" / filename
        if not source_path.exists():
            raise FileNotFoundError(f"Missing site icon source: {source_path}")
        destination_path = site_dir / filename
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
