#!/usr/bin/env python3
"""Build local module history refs and generated worktrees for the course."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


TAG_PREFIX = "python-functional-programming-module"
BRANCH_REF = "refs/heads/python-functional-programming-history"
MANIFESTS_DIRNAME = "manifests"


@dataclass(frozen=True)
class ModuleSource:
    module: str
    tag_name: str
    worktree_name: str
    root: Path
    snapshot_kind: str
    include_dirs: tuple[str, ...] = ()
    include_files: tuple[str, ...] = ()


def run(
    *args: str,
    cwd: Path,
    env: dict[str, str] | None = None,
    input_text: str | None = None,
) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        input=input_text,
        capture_output=True,
    )
    return completed.stdout.strip()


def is_executable(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IXUSR)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_snapshot_files(source: ModuleSource, *, root: Path | None = None) -> list[tuple[Path, str]]:
    snapshot_root = root or source.root
    files: list[tuple[Path, str]] = []
    ignored_dirs = {
        ".git",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".hypothesis",
        ".venv",
    }
    ignored_suffixes = {".pyc"}
    ignored_names = {".DS_Store"}

    def should_include(path: Path) -> bool:
        relative = path.relative_to(snapshot_root)
        return not (
            any(part in ignored_dirs for part in relative.parts)
            or path.suffix in ignored_suffixes
            or path.name in ignored_names
        )

    if source.include_dirs:
        for dirname in source.include_dirs:
            base_dir = snapshot_root / dirname
            if not base_dir.exists():
                continue
            for path in sorted(p for p in base_dir.rglob("*") if p.is_file() and should_include(p)):
                files.append((path, path.relative_to(snapshot_root).as_posix()))
    else:
        for path in sorted(p for p in snapshot_root.rglob("*") if p.is_file() and should_include(p)):
            files.append((path, path.relative_to(snapshot_root).as_posix()))
    for filename in source.include_files:
        path = snapshot_root / filename
        if path.exists() and should_include(path):
            files.append((path, filename))
    return files


def build_snapshot_manifest(
    source: ModuleSource,
    *,
    root: Path | None = None,
    worktree_root: Path | None = None,
) -> dict[str, object]:
    snapshot_root = root or source.root
    files = []
    for absolute_path, relative_path in iter_snapshot_files(source, root=snapshot_root):
        files.append(
            {
                "path": relative_path,
                "bytes": absolute_path.stat().st_size,
                "sha256": sha256(absolute_path),
            }
        )
    manifest: dict[str, object] = {
        "module": source.module,
        "tag": source.tag_name,
        "snapshot_kind": source.snapshot_kind,
        "source_root": snapshot_root.resolve().as_posix(),
        "file_count": len(files),
        "files": files,
    }
    if worktree_root is not None:
        manifest["worktree_root"] = worktree_root.resolve().as_posix()
    return manifest


def write_commit(repo_root: Path, source: ModuleSource, parent: str | None) -> str:
    with tempfile.NamedTemporaryFile(prefix="funcpipe-history-index-", delete=False) as handle:
        index_path = Path(handle.name)
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = str(index_path)
    try:
        run("git", "read-tree", "--empty", cwd=repo_root, env=env)
        for absolute_path, relative_path in iter_snapshot_files(source):
            mode = "100755" if is_executable(absolute_path) else "100644"
            blob = run("git", "hash-object", "-w", str(absolute_path), cwd=repo_root)
            run(
                "git",
                "update-index",
                "--add",
                "--cacheinfo",
                mode,
                blob,
                relative_path,
                cwd=repo_root,
                env=env,
            )
        tree = run("git", "write-tree", cwd=repo_root, env=env)
        args = ["git", "commit-tree", tree]
        if parent:
            args.extend(["-p", parent])
        message = f"{source.tag_name}: refresh module reference state"
        return run(*args, cwd=repo_root, input_text=message)
    finally:
        index_path.unlink(missing_ok=True)


def list_registered_worktrees(repo_root: Path) -> set[Path]:
    output = run("git", "worktree", "list", "--porcelain", cwd=repo_root)
    paths: set[Path] = set()
    for line in output.splitlines():
        if line.startswith("worktree "):
            paths.add(Path(line.removeprefix("worktree ")).resolve())
    return paths


def remove_generated_worktrees(repo_root: Path, worktrees_root: Path) -> None:
    registered = list_registered_worktrees(repo_root)
    if worktrees_root.exists():
        for path in sorted(worktrees_root.iterdir()):
            resolved = path.resolve()
            if resolved in registered:
                run("git", "worktree", "remove", "--force", str(path), cwd=repo_root)
            elif path.exists():
                shutil.rmtree(path)


def refresh_worktrees(repo_root: Path, out_dir: Path, modules: list[ModuleSource]) -> None:
    worktrees_root = out_dir / "worktrees"
    worktrees_root.mkdir(parents=True, exist_ok=True)
    remove_generated_worktrees(repo_root, worktrees_root)
    for source in modules:
        target = worktrees_root / source.worktree_name
        tag_ref = f"refs/tags/{source.tag_name}"
        run("git", "worktree", "add", "--force", "--detach", str(target), tag_ref, cwd=repo_root)


def write_manifests(out_dir: Path, modules: list[ModuleSource]) -> None:
    manifests_dir = out_dir / MANIFESTS_DIRNAME
    manifests_dir.mkdir(parents=True, exist_ok=True)
    worktrees_root = out_dir / "worktrees"
    for source in modules:
        worktree_root = worktrees_root / source.worktree_name
        manifest = build_snapshot_manifest(source, worktree_root=worktree_root)
        output = manifests_dir / f"module-{source.module}.json"
        output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_worktrees(out_dir: Path, modules: list[ModuleSource]) -> None:
    worktrees_root = out_dir / "worktrees"
    for source in modules:
        worktree_root = worktrees_root / source.worktree_name
        if not worktree_root.exists():
            raise FileNotFoundError(
                f"Missing generated worktree for module {source.module}: {worktree_root}"
            )
        source_manifest = build_snapshot_manifest(source)
        worktree_manifest = build_snapshot_manifest(source, root=worktree_root, worktree_root=worktree_root)
        if source_manifest["files"] != worktree_manifest["files"]:
            raise RuntimeError(
                f"Generated worktree for module {source.module} does not match the tracked snapshot source."
            )


def write_metadata(out_dir: Path, modules: list[ModuleSource], commits: dict[str, str]) -> None:
    metadata = {
        "program": "python-functional-programming",
        "generated_directory": "_history",
        "tag_prefix": TAG_PREFIX,
        "modules": [
            {
                "module": source.module,
                "tag": source.tag_name,
                "worktree": f"_history/worktrees/{source.worktree_name}",
                "manifest": f"_history/{MANIFESTS_DIRNAME}/module-{source.module}.json",
                "commit": commits[source.module],
                "snapshot_kind": source.snapshot_kind,
                "source": str(source.root),
            }
            for source in modules
        ],
    }
    (out_dir / "module-history.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    route_lines = [
        "Generated module history route:",
        "  1. Run make PROGRAM=python-programming/python-functional-programming history-refresh from the repository root, or make history-refresh from the course or capstone directory.",
        "  2. Read _history/manifests/module-XX.json to see the exact file inventory and source root for that snapshot.",
        "  3. Open _history/worktrees/module-XX for the generated git worktree that was verified against the manifest.",
        "  4. Use the matching python-functional-programming-module-XX tag when you want the exact ref name.",
        "  5. Re-run make history-refresh after updating a module reference state or the live capstone endpoint.",
        "",
        "Available refs:",
    ]
    route_lines.extend(
        "  - "
        f"{source.module}: {source.tag_name} -> _history/worktrees/{source.worktree_name} "
        f"({_history_path(MANIFESTS_DIRNAME, source.module)})"
        for source in modules
    )
    (out_dir / "route.txt").write_text("\n".join(route_lines) + "\n", encoding="utf-8")


def _history_path(dirname: str, module: str) -> str:
    return f"_history/{dirname}/module-{module}.json"


def build_history(repo_root: Path, capstone_root: Path, out_dir: Path) -> None:
    reference_root = capstone_root / "module-reference-states"
    modules = [
        ModuleSource(
            module=f"{number:02d}",
            tag_name=f"{TAG_PREFIX}-{number:02d}",
            worktree_name=f"module-{number:02d}",
            root=reference_root / f"module-{number:02d}",
            snapshot_kind="tracked-reference-state",
        )
        for number in range(1, 10)
    ]
    modules.append(
        ModuleSource(
            module="10",
            tag_name=f"{TAG_PREFIX}-10",
            worktree_name="module-10",
            root=capstone_root,
            snapshot_kind="live-capstone-endpoint",
            include_dirs=("src", "tests", "scripts"),
            include_files=(
                "README.md",
                "ARCHITECTURE.md",
                "TOUR.md",
                "PROOF_GUIDE.md",
                "PACKAGE_GUIDE.md",
                "TEST_GUIDE.md",
                "WALKTHROUGH_GUIDE.md",
                "EXTENSION_GUIDE.md",
                "pyproject.toml",
                "Makefile",
            ),
        )
    )

    commits: dict[str, str] = {}
    parent: str | None = None
    for source in modules:
        commit = write_commit(repo_root, source, parent)
        run("git", "update-ref", f"refs/tags/{source.tag_name}", commit, cwd=repo_root)
        commits[source.module] = commit
        parent = commit
    if parent:
        run("git", "update-ref", BRANCH_REF, parent, cwd=repo_root)

    out_dir.mkdir(parents=True, exist_ok=True)
    refresh_worktrees(repo_root, out_dir, modules)
    verify_worktrees(out_dir, modules)
    write_manifests(out_dir, modules)
    write_metadata(out_dir, modules, commits)
    run("git", "worktree", "prune", cwd=repo_root)


def verify_history(capstone_root: Path, out_dir: Path) -> None:
    reference_root = capstone_root / "module-reference-states"
    modules = [
        ModuleSource(
            module=f"{number:02d}",
            tag_name=f"{TAG_PREFIX}-{number:02d}",
            worktree_name=f"module-{number:02d}",
            root=reference_root / f"module-{number:02d}",
            snapshot_kind="tracked-reference-state",
        )
        for number in range(1, 10)
    ]
    modules.append(
        ModuleSource(
            module="10",
            tag_name=f"{TAG_PREFIX}-10",
            worktree_name="module-10",
            root=capstone_root,
            snapshot_kind="live-capstone-endpoint",
            include_dirs=("src", "tests", "scripts"),
            include_files=(
                "README.md",
                "ARCHITECTURE.md",
                "TOUR.md",
                "PROOF_GUIDE.md",
                "PACKAGE_GUIDE.md",
                "TEST_GUIDE.md",
                "WALKTHROUGH_GUIDE.md",
                "EXTENSION_GUIDE.md",
                "pyproject.toml",
                "Makefile",
            ),
        )
    )
    verify_worktrees(out_dir, modules)
    write_manifests(out_dir, modules)
    write_metadata(
        out_dir,
        modules,
        commits={
            source.module: run("git", "rev-parse", f"refs/tags/{source.tag_name}", cwd=capstone_root)
            for source in modules
        },
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        default="_history",
        help="Generated history output directory relative to the capstone root.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Verify existing generated worktrees against the tracked snapshot sources.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    capstone_root = Path(__file__).resolve().parents[1]
    repo_root = Path(run("git", "rev-parse", "--show-toplevel", cwd=capstone_root))
    out_dir = (capstone_root / args.out_dir).resolve()
    if args.verify_only:
        verify_history(capstone_root=capstone_root, out_dir=out_dir)
        return
    build_history(repo_root=repo_root, capstone_root=capstone_root, out_dir=out_dir)


if __name__ == "__main__":
    main()
