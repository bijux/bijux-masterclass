from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "write_bundle_manifest.py"
SPEC = importlib.util.spec_from_file_location("bundle_manifest_writer", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_build_manifest_records_stable_sorted_paths_and_hashes(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    bundle_dir.mkdir()
    (bundle_dir / "b.txt").write_text("beta\n", encoding="utf-8")
    nested = bundle_dir / "nested"
    nested.mkdir()
    (nested / "a.txt").write_text("alpha\n", encoding="utf-8")

    manifest = MODULE.build_manifest(bundle_dir)

    assert manifest["file_count"] == 2
    assert [item["path"] for item in manifest["files"]] == [
        "b.txt",
        "nested/a.txt",
    ]
    assert manifest["files"][0]["sha256"] == hashlib.sha256(b"beta\n").hexdigest()
    assert manifest["files"][1]["sha256"] == hashlib.sha256(b"alpha\n").hexdigest()


def test_main_writes_bundle_manifest_json(tmp_path: Path, monkeypatch) -> None:
    bundle_dir = tmp_path / "bundle"
    bundle_dir.mkdir()
    (bundle_dir / "route.txt").write_text("saved review route\n", encoding="utf-8")
    output = tmp_path / "bundle-manifest.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "write_bundle_manifest.py",
            "--bundle-dir",
            str(bundle_dir),
            "--output",
            str(output),
        ],
    )

    MODULE.main()

    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["file_count"] == 1
    assert manifest["files"][0]["path"] == "route.txt"
