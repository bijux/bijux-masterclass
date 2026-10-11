#!/usr/bin/env python3
"""Select the smallest program validation matrix justified by changed paths."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

if __package__:
    from .program_qualification.profiles import FAST_TESTS
else:
    from program_qualification.profiles import FAST_TESTS


@dataclass(frozen=True)
class ValidationTarget:
    name: str
    command: str
    program_prefix: str | None = None

    def matrix_entry(self, profile: str | None = None) -> dict[str, str]:
        if profile is None:
            return {
                "name": self.name,
                "command": self.command,
                "qualification": "false",
            }
        assert self.program_prefix is not None
        program = self.program_prefix.removeprefix("programs/").rstrip("/")
        command = self.command
        persisted = program in FAST_TESTS
        if persisted:
            command = f"make PROGRAM={program} program-validation PROGRAM_VALIDATION_PROFILE={profile}"
        return {
            "name": f"{self.name}-{profile}",
            "command": command,
            "qualification": str(persisted).lower(),
            "program": program,
        }


SERIES_SITE = ValidationTarget(
    name="series-site",
    command="make docs-nav-check",
)

ROOT_CONTRACT = ValidationTarget(
    name="root-contract",
    command="make help >/dev/null\nmake programs >/dev/null\nmake program-help >/dev/null",
)

PROGRAM_TARGETS = (
    ValidationTarget(
        name="deep-dive-make",
        program_prefix="programs/reproducible-research/deep-dive-make/",
        command=("make PROGRAM=reproducible-research/deep-dive-make test"),
    ),
    ValidationTarget(
        name="deep-dive-snakemake",
        program_prefix="programs/reproducible-research/deep-dive-snakemake/",
        command=(
            "make -C programs/reproducible-research/deep-dive-snakemake/capstone "
            "bootstrap-confirm"
        ),
    ),
    ValidationTarget(
        name="deep-dive-dvc",
        program_prefix="programs/reproducible-research/deep-dive-dvc/",
        command=("make PROGRAM=reproducible-research/deep-dive-dvc test"),
    ),
    ValidationTarget(
        name="python-functional-programming",
        program_prefix="programs/python-programming/python-functional-programming/",
        command=("make PROGRAM=python-programming/python-functional-programming test"),
    ),
    ValidationTarget(
        name="python-object-oriented-programming",
        program_prefix="programs/python-programming/python-object-oriented-programming/",
        command=(
            "make PROGRAM=python-programming/python-object-oriented-programming test"
        ),
    ),
    ValidationTarget(
        name="python-meta-programming",
        program_prefix="programs/python-programming/python-meta-programming/",
        command=("make PROGRAM=python-programming/python-meta-programming test"),
    ),
)

PROGRAM_DOCUMENTATION_TARGETS = tuple(
    ValidationTarget(
        name=f"{target.name}-documentation",
        program_prefix=target.program_prefix,
        command=f"make PROGRAM={target.program_prefix.removeprefix('programs/').rstrip('/')} docs-build",
    )
    for target in PROGRAM_TARGETS
)

SHARED_DOCUMENTATION_PATHS = {
    "mkdocs.shared.yml",
    "makes/docs.mk",
    "makes/bijux-docs.mk",
    "makes/series-docs.mk",
    "scripts/docs_environment.py",
    "scripts/sync_course_nav.py",
    "scripts/serve_docs.py",
}

SHARED_VALIDATION_PATHS = {
    ".github/workflows/program-validation.yml",
    "makes/root.mk",
    "makes/program.mk",
    "scripts/program_validation.py",
}
SHARED_VALIDATION_PREFIXES = ("scripts/program_qualification/",)
SHARED_DOCUMENTATION_PREFIXES = (
    "configs/docs/",
    "docs/hooks/",
    ".bijux/shared/bijux-docs/",
)
ROOT_CONTRACT_PATHS = {
    "Makefile",
    "makes/bijux-docs.mk",
    "makes/bijux-std.mk",
    "makes/docs.mk",
    "makes/program.mk",
    "makes/root.mk",
    "makes/series-docs.mk",
}
SERIES_SITE_PATHS = {
    "mkdocs.yml",
    "makes/bijux-docs.mk",
    "makes/series-docs.mk",
    "scripts/render_root_mkdocs.py",
    "scripts/sync_series_docs.py",
    "scripts/docs_nav.py",
    "scripts/check_masterclass_navigation.py",
    "scripts/check_masterclass_library_tree.py",
    "scripts/check_masterclass_shell.py",
}
SERIES_SITE_PREFIXES = (
    "scripts/catalogue/",
    ".bijux/shared/bijux-docs/",
    "docs/",
)
PROGRAM_DOCUMENTATION_PARTS = (
    "/course-book/",
    "/capstone/docs/",
)


def normalize_paths(paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        normalized
        for raw_path in paths
        if (normalized := raw_path.strip().removeprefix("./"))
    )


def has_prefix(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path.startswith(prefix) for prefix in prefixes)


def affects_all_programs(path: str) -> bool:
    return path in SHARED_VALIDATION_PATHS or has_prefix(
        path, SHARED_VALIDATION_PREFIXES
    )


def is_program_documentation(path: str, prefix: str) -> bool:
    relative = path.removeprefix(prefix)
    return relative in {"README.md", "mkdocs.yml"} or relative.startswith(
        ("course-book/", "capstone/docs/")
    )


def affects_series_site(path: str) -> bool:
    if path in SERIES_SITE_PATHS or has_prefix(path, SERIES_SITE_PREFIXES):
        return True
    if path in {"programs/README.md", "programs/reproducible-research/README.md"}:
        return True
    if path == "programs/python-programming/README.md":
        return True
    if not path.startswith("programs/"):
        return False
    return path.endswith(("/README.md", "/mkdocs.yml")) or any(
        part in path for part in PROGRAM_DOCUMENTATION_PARTS
    )


def select_validation_targets(
    paths: Iterable[str], *, select_all: bool = False
) -> list[dict[str, str]]:
    changed_paths = normalize_paths(paths)
    selected_names: set[str] = set()

    if select_all or any(affects_all_programs(path) for path in changed_paths):
        selected_names.update(target.name for target in PROGRAM_TARGETS)
        selected_names.update(target.name for target in PROGRAM_DOCUMENTATION_TARGETS)
        selected_names.add(ROOT_CONTRACT.name)
        selected_names.add(SERIES_SITE.name)
    else:
        for target, documentation in zip(
            PROGRAM_TARGETS, PROGRAM_DOCUMENTATION_TARGETS
        ):
            assert target.program_prefix is not None
            affected = [
                path for path in changed_paths if path.startswith(target.program_prefix)
            ]
            if affected:
                selected_names.add(documentation.name)
            if any(
                not is_program_documentation(path, target.program_prefix)
                for path in affected
            ):
                selected_names.add(target.name)
        if any(
            path in SHARED_DOCUMENTATION_PATHS
            or has_prefix(path, SHARED_DOCUMENTATION_PREFIXES)
            for path in changed_paths
        ):
            selected_names.update(
                target.name for target in PROGRAM_DOCUMENTATION_TARGETS
            )
            selected_names.update({ROOT_CONTRACT.name, SERIES_SITE.name})
        if any(path in ROOT_CONTRACT_PATHS for path in changed_paths):
            selected_names.add(ROOT_CONTRACT.name)
        if any(affects_series_site(path) for path in changed_paths):
            selected_names.add(SERIES_SITE.name)

    ordered_targets = (
        ROOT_CONTRACT,
        SERIES_SITE,
        *PROGRAM_DOCUMENTATION_TARGETS,
        *PROGRAM_TARGETS,
    )
    return [
        target.matrix_entry(
            ("full" if select_all else "fast") if target in PROGRAM_TARGETS else None
        )
        for target in ordered_targets
        if target.name in selected_names
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed-file-list",
        type=Path,
        help="newline-delimited repository paths changed by the pull request",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="select_all",
        help="select every validation target for a manual full run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.select_all and args.changed_file_list is None:
        raise SystemExit("--changed-file-list is required unless --all is used")

    paths: list[str] = []
    if args.changed_file_list is not None:
        paths = args.changed_file_list.read_text(encoding="utf-8").splitlines()

    matrix = {"include": select_validation_targets(paths, select_all=args.select_all)}
    print(json.dumps(matrix, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
