from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "scripts" / "build_module_history.py"
SPEC = importlib.util.spec_from_file_location("build_module_history", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

ModuleSource = MODULE.ModuleSource
build_snapshot_manifest = MODULE.build_snapshot_manifest
verify_worktrees = MODULE.verify_worktrees


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_build_snapshot_manifest_respects_include_filters(tmp_path: Path) -> None:
    source_root = tmp_path / "module-10"
    write(source_root / "src" / "pkg" / "__init__.py", "print('src')\n")
    write(source_root / "tests" / "test_sample.py", "def test_ok():\n    assert True\n")
    write(source_root / "scripts" / "tool.py", "print('tool')\n")
    write(source_root / "README.md", "# Snapshot\n")
    write(source_root / "notes.txt", "ignore me\n")

    source = ModuleSource(
        module="10",
        tag_name="python-functional-programming-module-10",
        worktree_name="module-10",
        root=source_root,
        snapshot_kind="live-capstone-endpoint",
        include_dirs=("src", "tests", "scripts"),
        include_files=("README.md",),
    )

    manifest = build_snapshot_manifest(source)

    assert manifest["snapshot_kind"] == "live-capstone-endpoint"
    assert manifest["file_count"] == 4
    assert [item["path"] for item in manifest["files"]] == [
        "src/pkg/__init__.py",
        "tests/test_sample.py",
        "scripts/tool.py",
        "README.md",
    ]


def test_verify_worktrees_accepts_exact_match_and_ignores_git_file(tmp_path: Path) -> None:
    source_root = tmp_path / "reference" / "module-01"
    worktree_root = tmp_path / "_history" / "worktrees" / "module-01"
    write(source_root / "src" / "pkg.py", "VALUE = 1\n")
    write(source_root / "tests" / "test_pkg.py", "def test_value():\n    assert True\n")
    write(worktree_root / "src" / "pkg.py", "VALUE = 1\n")
    write(worktree_root / "tests" / "test_pkg.py", "def test_value():\n    assert True\n")
    write(worktree_root / ".git", "gitdir: /tmp/fake\n")

    source = ModuleSource(
        module="01",
        tag_name="python-functional-programming-module-01",
        worktree_name="module-01",
        root=source_root,
        snapshot_kind="tracked-reference-state",
    )

    verify_worktrees(tmp_path / "_history", [source])


def test_verify_worktrees_rejects_mismatch(tmp_path: Path) -> None:
    source_root = tmp_path / "reference" / "module-02"
    worktree_root = tmp_path / "_history" / "worktrees" / "module-02"
    write(source_root / "src" / "pkg.py", "VALUE = 1\n")
    write(worktree_root / "src" / "pkg.py", "VALUE = 2\n")

    source = ModuleSource(
        module="02",
        tag_name="python-functional-programming-module-02",
        worktree_name="module-02",
        root=source_root,
        snapshot_kind="tracked-reference-state",
    )

    with pytest.raises(RuntimeError, match="module 02"):
        verify_worktrees(tmp_path / "_history", [source])
