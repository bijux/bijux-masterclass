from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts"


def copy_blueprint() -> tempfile.TemporaryDirectory[str]:
    ARTIFACTS.mkdir(exist_ok=True)
    directory = tempfile.TemporaryDirectory(dir=ARTIFACTS)
    target = Path(directory.name)
    shutil.copytree(ROOT / "manifests", target / "manifests")
    shutil.copytree(ROOT / "programs", target / "programs")
    shutil.copy2(ROOT / "ALL_3000_MODULES.md", target)
    return directory
