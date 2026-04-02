from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_bundle_manifest_script_writes_a_stable_inventory(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    bundle_dir.mkdir()
    (bundle_dir / "alpha.txt").write_text("alpha\n", encoding="utf-8")
    (bundle_dir / "beta.txt").write_text("beta\n", encoding="utf-8")
    output = tmp_path / "manifest.json"

    subprocess.run(
        [
            "python3",
            "scripts/write_bundle_manifest.py",
            "--bundle-dir",
            str(bundle_dir),
            "--output",
            str(output),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
    )

    manifest = json.loads(output.read_text(encoding="utf-8"))

    assert manifest["file_count"] == 2
    assert {item["path"] for item in manifest["files"]} == {"alpha.txt", "beta.txt"}
    assert all("sha256" in item for item in manifest["files"])
