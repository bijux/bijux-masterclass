"""Review-oriented CLI for inspecting the FuncPipe capstone."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PACKAGE_GROUPS: tuple[dict[str, Any], ...] = (
    {
        "name": "functional-core",
        "paths": [
            "src/funcpipe_rag/fp",
            "src/funcpipe_rag/result",
            "src/funcpipe_rag/tree",
            "src/funcpipe_rag/streaming",
        ],
        "purpose": "Reusable algebra, containers, folds, and lazy stream behavior.",
        "tests": [
            "tests/unit/fp",
            "tests/unit/result",
            "tests/unit/tree",
            "tests/unit/streaming",
        ],
    },
    {
        "name": "rag-model",
        "paths": [
            "src/funcpipe_rag/core",
            "src/funcpipe_rag/rag",
            "src/funcpipe_rag/rag/domain",
        ],
        "purpose": "RAG-specific value shapes, stages, and domain assembly logic.",
        "tests": [
            "tests/unit/rag",
            "tests/unit/rag/domain",
        ],
    },
    {
        "name": "orchestration-and-policy",
        "paths": [
            "src/funcpipe_rag/pipelines",
            "src/funcpipe_rag/policies",
        ],
        "purpose": "Configured pipeline assembly and explicit runtime policy choices.",
        "tests": [
            "tests/unit/pipelines",
            "tests/unit/policies",
        ],
    },
    {
        "name": "effect-boundaries",
        "paths": [
            "src/funcpipe_rag/domain",
            "src/funcpipe_rag/domain/effects",
            "src/funcpipe_rag/boundaries",
            "src/funcpipe_rag/infra",
        ],
        "purpose": "Capabilities, shells, adapters, and concrete runtime edges.",
        "tests": [
            "tests/unit/domain",
            "tests/unit/boundaries",
            "tests/unit/infra/adapters",
        ],
    },
    {
        "name": "interop",
        "paths": [
            "src/funcpipe_rag/interop",
        ],
        "purpose": "Compatibility layers for stdlib and external functional helpers.",
        "tests": [
            "tests/unit/interop",
        ],
    },
)

TEST_GROUPS: tuple[dict[str, Any], ...] = (
    {
        "name": "algebra-and-laws",
        "paths": [
            "tests/unit/fp/laws",
            "tests/unit/result",
            "tests/unit/tree",
        ],
        "proves": "Functional laws, folds, and algebraic container behavior.",
    },
    {
        "name": "functional-toolkit",
        "paths": [
            "tests/unit/fp",
            "tests/unit/streaming",
        ],
        "proves": "Pure helpers, local reasoning, and streaming composition.",
    },
    {
        "name": "application-model",
        "paths": [
            "tests/unit/rag",
            "tests/unit/rag/domain",
        ],
        "proves": "RAG assembly, stage composition, and domain value contracts.",
    },
    {
        "name": "pipeline-and-policy",
        "paths": [
            "tests/unit/pipelines",
            "tests/unit/policies",
        ],
        "proves": "Configured pipeline assembly and operational policy boundaries.",
    },
    {
        "name": "edges-and-effects",
        "paths": [
            "tests/unit/domain",
            "tests/unit/boundaries",
            "tests/unit/infra/adapters",
            "tests/unit/interop",
        ],
        "proves": "Async pressure, capabilities, serialization, storage, and interop edges.",
    },
)

PROOF_ROUTES: tuple[dict[str, str], ...] = (
    {
        "name": "demo",
        "command": "make demo",
        "meaning": "Build the learner-facing walkthrough bundle with the shared catalog verb.",
    },
    {
        "name": "test",
        "command": "make test",
        "meaning": "Run the executable test suite for behavioral and law-based proof.",
    },
    {
        "name": "tour",
        "command": "make tour",
        "meaning": "Build the capstone proof bundle for human review.",
    },
    {
        "name": "proof",
        "command": "make proof",
        "meaning": "Run the sanctioned learner-facing end-to-end proof route.",
    },
)


def _count_python_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for candidate in path.rglob("*.py") if candidate.is_file())


def build_summary(project_root: Path) -> dict[str, Any]:
    package_groups: list[dict[str, Any]] = []
    for group in PACKAGE_GROUPS:
        paths = [project_root / rel for rel in group["paths"]]
        package_groups.append(
            {
                **group,
                "python_file_count": sum(_count_python_files(path) for path in paths),
            }
        )

    test_groups: list[dict[str, Any]] = []
    for group in TEST_GROUPS:
        paths = [project_root / rel for rel in group["paths"]]
        test_groups.append(
            {
                **group,
                "python_file_count": sum(_count_python_files(path) for path in paths),
            }
        )

    return {
        "project_root": project_root.resolve().as_posix(),
        "package_groups": package_groups,
        "test_groups": test_groups,
        "proof_routes": list(PROOF_ROUTES),
    }


def render_text(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("FuncPipe review summary")
    lines.append(f"project_root: {summary['project_root']}")
    lines.append("")
    lines.append("Package groups:")
    for group in summary["package_groups"]:
        lines.append(
            f"- {group['name']}: {group['python_file_count']} python files; {group['purpose']}"
        )
        lines.append(f"  paths: {', '.join(group['paths'])}")
        lines.append(f"  tests: {', '.join(group['tests'])}")
    lines.append("")
    lines.append("Test groups:")
    for group in summary["test_groups"]:
        lines.append(
            f"- {group['name']}: {group['python_file_count']} python files; {group['proves']}"
        )
        lines.append(f"  paths: {', '.join(group['paths'])}")
    lines.append("")
    lines.append("Proof routes:")
    for route in summary["proof_routes"]:
        lines.append(f"- {route['name']}: {route['command']} -> {route['meaning']}")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="funcpipe-rag-review")
    parser.add_argument(
        "command",
        choices=("summary",),
        nargs="?",
        default="summary",
        help="Inspection report to render.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="text",
        help="Output format for the selected report.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Capstone project root. Defaults to the current working directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = build_summary(args.project_root)
    if args.format == "json":
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(render_text(summary), end="")
    return 0


__all__ = ["build_summary", "main", "parse_args", "render_text"]
