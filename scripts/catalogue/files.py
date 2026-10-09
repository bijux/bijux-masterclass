"""Capture original catalogue inputs and verify/materialize a pure source plan."""
from __future__ import annotations
from collections.abc import Mapping
from hashlib import sha256
import os
from pathlib import Path
import shutil
import stat
import tempfile
from scripts.catalogue.source_plan import CataloguePlan, PlanError, safe_path

SKIP_PARTS = {".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache", ".venv"}


def regular_path(root: Path, relative: str) -> Path:
    safe_path(relative)
    if root.is_symlink():
        raise PlanError("catalogue root cannot be a symlink")
    path = root / relative
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink():
            raise PlanError(f"catalogue path cannot use a symlink: {relative}")
        if ancestor == root:
            break
    return path


def capture_sources(root: Path) -> dict[str, bytes]:
    """Read original bytes only; generated docs/configuration are never authority."""
    sources = {}
    def capture(name):
        path = regular_path(root, name)
        if not path.is_file():
            raise PlanError(f"missing original source: {name}")
        sources[name] = path.read_bytes()
    for name in ("mkdocs.yml", "mkdocs.shared.yml"):
        capture(name)
    programs = regular_path(root, "programs")
    if not programs.is_dir():
        raise PlanError("missing original source: programs")
    for directory, folders, names in os.walk(programs, followlinks=False):
        current = Path(directory)
        folders[:] = sorted(name for name in folders if name not in SKIP_PARTS)
        for name in folders:
            regular_path(root, (current / name).relative_to(root).as_posix())
        for name in sorted(names):
            if name.endswith(".md") or name == "mkdocs.yml":
                capture((current / name).relative_to(root).as_posix())
    for family in sorted(path for path in programs.iterdir() if path.is_dir() and path.name not in SKIP_PARTS):
        capture((family / "README.md").relative_to(root).as_posix())
    for name in ("scripts/sync_series_docs.py", "scripts/render_root_mkdocs.py", "scripts/docs_nav.py"):
        capture(name)
    for path in sorted((root / "scripts/catalogue").rglob("*.py")):
        capture(path.relative_to(root).as_posix())
    return sources


def verify_sources(plan: CataloguePlan, root: Path) -> None:
    actual = tuple((key, sha256(content).hexdigest()) for key, content in sorted(capture_sources(root).items()))
    if actual != plan.source_hashes:
        raise PlanError("original catalogue inputs changed after planning")


def _document_files(plan: CataloguePlan, root: Path) -> dict[str, bytes]:
    actual = {}
    roots = [regular_path(root, "docs/index.md"), *(regular_path(root, f"docs/{family}") for family in plan.families)]
    for owned in roots:
        paths = sorted(owned.rglob("*")) if owned.is_dir() else [owned]
        for path in paths:
            relative = path.relative_to(root).as_posix()
            regular_path(root, relative)
            if path.is_file():
                actual[relative] = path.read_bytes()
            elif path.exists() and not path.is_dir():
                raise PlanError(f"unsupported catalogue output: {relative}")
    return actual


def verify_outputs(plan: CataloguePlan, root: Path, *, configuration=True) -> None:
    """Reject missing, extra or modified derived bytes without relabeling them tracked."""
    expected = {item.destination: item.content for item in plan.documents}
    if _document_files(plan, root) != expected:
        raise PlanError("derived catalogue documents do not match the original-source plan")
    if configuration:
        path = regular_path(root, plan.configuration.destination)
        if not path.is_file() or path.read_bytes() != plan.configuration.content:
            raise PlanError("derived catalogue configuration does not match its captured owner")


def _reviewed_removals(actual: dict[str, bytes], expected: set[str],
                       previous_outputs: Mapping[str, bytes]) -> None:
    """Unknown bytes cannot become deletion authority merely by living under docs/."""
    for name, content in actual.items():
        if name in expected:
            continue
        if name not in previous_outputs or previous_outputs[name] != content:
            raise PlanError(f"unowned catalogue output would be deleted: {name}")


def _atomic_write(root: Path, relative: str, content: bytes) -> None:
    """Replace an owned output inode without writing through an existing alias."""
    path = regular_path(root, relative)
    mode = 0o644
    if path.exists():
        if not path.is_file():
            raise PlanError(f"catalogue output is not a regular file: {relative}")
        metadata = path.stat()
        if metadata.st_nlink != 1:
            raise PlanError(f"catalogue output cannot use a hardlink: {relative}")
        mode = stat.S_IMODE(metadata.st_mode)
    path.parent.mkdir(parents=True, exist_ok=True)
    regular_path(root, relative)
    pending = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent,
                                         prefix=".catalogue-", delete=False) as output:
            pending = Path(output.name)
            output.write(content)
        pending.chmod(mode)
        os.replace(pending, path)
    finally:
        if pending is not None:
            pending.unlink(missing_ok=True)


def write_documents(plan: CataloguePlan, root: Path, *,
                    previous_outputs: Mapping[str, bytes] | None = None) -> None:
    """Materialize owned routes; remove stale bytes only with explicit prior ownership.

    Callers may supply a reviewed prior plan's output_bytes() for changed route sets.
    Matching prior bytes confirm removal ownership, not Git or publication authority.
    """
    verify_sources(plan, root)
    expected = {document.destination for document in plan.documents}
    previous_outputs = dict(previous_outputs or {})
    for name, content in previous_outputs.items():
        safe_path(name)
        if not isinstance(content, bytes):
            raise PlanError(f"prior catalogue ownership is not captured bytes: {name}")
    actual = _document_files(plan, root)
    _reviewed_removals(actual, expected, previous_outputs)
    for document in plan.documents:
        path = regular_path(root, document.destination)
        if path.exists() and not path.is_file():
            raise PlanError(f"catalogue output is not a regular file: {document.destination}")
    legacy = regular_path(root, "docs/library")
    if legacy.exists():
        if not legacy.is_dir():
            raise PlanError("legacy catalogue output is not a directory: docs/library")
        legacy_files = {}
        for path in legacy.rglob("*"):
            name = path.relative_to(root).as_posix()
            regular_path(root, name)
            if path.is_file():
                legacy_files[name] = path.read_bytes()
            elif path.exists() and not path.is_dir():
                raise PlanError(f"unsupported catalogue output: {name}")
        _reviewed_removals(legacy_files, set(), previous_outputs)
    for family in plan.families:
        target = regular_path(root, f"docs/{family}")
        if target.exists():
            shutil.rmtree(target)
    index = regular_path(root, "docs/index.md")
    if index.exists():
        index.unlink()
    if legacy.exists():
        shutil.rmtree(legacy)
    for document in plan.documents:
        _atomic_write(root, document.destination, document.content)
    verify_sources(plan, root)
    verify_outputs(plan, root, configuration=False)


def write_configuration(plan: CataloguePlan, root: Path) -> None:
    verify_sources(plan, root)
    verify_outputs(plan, root, configuration=False)
    _atomic_write(root, plan.configuration.destination, plan.configuration.content)
    verify_sources(plan, root)
    verify_outputs(plan, root)
