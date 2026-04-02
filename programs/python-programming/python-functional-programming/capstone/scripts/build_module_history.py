#!/usr/bin/env python3
"""Build local module history refs and generated worktrees for the course."""

from __future__ import annotations

import argparse
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


@dataclass(frozen=True)
class ModuleSource:
    module: str
    tag_name: str
    worktree_name: str
    root: Path
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


def iter_tracked_files(source: ModuleSource) -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    if source.include_dirs:
        for dirname in source.include_dirs:
            base_dir = source.root / dirname
            if not base_dir.exists():
                continue
            for path in sorted(p for p in base_dir.rglob("*") if p.is_file()):
                files.append((path, path.relative_to(source.root).as_posix()))
    else:
        for path in sorted(p for p in source.root.rglob("*") if p.is_file()):
            files.append((path, path.relative_to(source.root).as_posix()))
    for filename in source.include_files:
        path = source.root / filename
        if path.exists():
            files.append((path, filename))
    return files


def write_commit(repo_root: Path, source: ModuleSource, parent: str | None) -> str:
    with tempfile.NamedTemporaryFile(prefix="funcpipe-history-index-", delete=False) as handle:
        index_path = Path(handle.name)
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = str(index_path)
    try:
        run("git", "read-tree", "--empty", cwd=repo_root, env=env)
        for absolute_path, relative_path in iter_tracked_files(source):
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
                "commit": commits[source.module],
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
        "  1. Run make history-refresh from the capstone or program directory.",
        "  2. Open _history/worktrees/module-XX for the module you want to compare.",
        "  3. Use the matching python-functional-programming-module-XX tag when you want the exact ref name.",
        "  4. Re-run make history-refresh after updating a module reference state or the live capstone endpoint.",
        "",
        "Available refs:",
    ]
    route_lines.extend(
        f"  - {source.module}: {source.tag_name} -> _history/worktrees/{source.worktree_name}"
        for source in modules
    )
    (out_dir / "route.txt").write_text("\n".join(route_lines) + "\n", encoding="utf-8")


def build_history(repo_root: Path, capstone_root: Path, out_dir: Path) -> None:
    reference_root = capstone_root / "module-reference-states"
    modules = [
        ModuleSource(
            module=f"{number:02d}",
            tag_name=f"{TAG_PREFIX}-{number:02d}",
            worktree_name=f"module-{number:02d}",
            root=reference_root / f"module-{number:02d}",
        )
        for number in range(1, 10)
    ]
    modules.append(
        ModuleSource(
            module="10",
            tag_name=f"{TAG_PREFIX}-10",
            worktree_name="module-10",
            root=capstone_root,
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
    write_metadata(out_dir, modules, commits)
    run("git", "worktree", "prune", cwd=repo_root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        default="_history",
        help="Generated history output directory relative to the capstone root.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    capstone_root = Path(__file__).resolve().parents[1]
    repo_root = Path(run("git", "rev-parse", "--show-toplevel", cwd=capstone_root))
    out_dir = (capstone_root / args.out_dir).resolve()
    build_history(repo_root=repo_root, capstone_root=capstone_root, out_dir=out_dir)


if __name__ == "__main__":
    main()
