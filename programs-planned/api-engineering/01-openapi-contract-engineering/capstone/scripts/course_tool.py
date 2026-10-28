#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from spec_tools import (
    CourseValidationError,
    ROOT,
    SPEC_DIR,
    apply_overlay,
    bundle_document,
    compare_contracts,
    ensure_no_errors,
    load_yaml,
    operation_ledger,
    validate_arazzo,
    validate_examples,
    validate_fixture_manifest,
    validate_openapi_structure,
    validate_overlay,
    validate_references,
    write_yaml,
)

COURSE = ROOT.parent
DIST = SPEC_DIR / "dist"
REPORTS = ROOT / "reports"

_BUNDLE_CACHE: dict[Path, Any] = {}


def _bundled(entry: Path) -> Any:
    """Return an isolated copy of a bundle cached for this proof process."""
    key = entry.resolve()
    if key not in _BUNDLE_CACHE:
        _BUNDLE_CACHE[key] = bundle_document(key)
    return copy.deepcopy(_BUNDLE_CACHE[key])


def _print_ok(label: str, detail: str = "") -> None:
    suffix = f" — {detail}" if detail else ""
    print(f"PASS {label}{suffix}")


def _entry(frontier: bool = False) -> Path:
    return SPEC_DIR / ("openapi-3.2.yaml" if frontier else "openapi.yaml")


def cmd_structure(_: argparse.Namespace) -> None:
    required_root = [
        COURSE / "README.md",
        COURSE / "Makefile",
        COURSE / "mkdocs.yml",
        COURSE / "course-book/index.md",
        ROOT / "README.md",
        ROOT / "Makefile",
        SPEC_DIR / "openapi.yaml",
        SPEC_DIR / "openapi-3.2.yaml",
        ROOT / "tests/tooling/capability-cases.yaml",
    ]
    missing = [str(path.relative_to(COURSE)) for path in required_root if not path.is_file()]
    module_dirs = sorted((COURSE / "course-book").glob("module-[0-9][0-9]-*"))
    if len(module_dirs) != 11:
        missing.append(f"expected orientation plus ten module directories, found {len(module_dirs)}")
    expected_module_files = {
        'index.md', 'exercises.md', 'exercise-answers.md', 'lab.md', 'checkpoint.md'
    }
    for directory in module_dirs:
        if directory.name.startswith("module-00"):
            continue
        present = {path.name for path in directory.glob("*.md")}
        absent = sorted(expected_module_files - present)
        if absent:
            missing.append(f"{directory.name}: missing {', '.join(absent)}")
    ensure_no_errors("course structure", missing)
    _print_ok("course structure", f"{len(module_dirs)} module directories")


def cmd_parse(_: argparse.Namespace) -> None:
    for frontier, version in ((False, "3.1.2"), (True, "3.2.0")):
        spec = load_yaml(_entry(frontier))
        ensure_no_errors(
            f"OpenAPI {version} structure",
            validate_openapi_structure(_bundled(_entry(frontier)), version),
        )
        _print_ok(f"parse OpenAPI {version}")


def cmd_refs(_: argparse.Namespace) -> None:
    for frontier in (False, True):
        entry = _entry(frontier)
        ensure_no_errors(entry.name, validate_references(entry))
        _print_ok("reference resolution", entry.name)


def _bundle_one(entry: Path, output: Path) -> dict[str, Any]:
    bundled = _bundled(entry)
    write_yaml(output, bundled)
    return bundled


def cmd_bundle(_: argparse.Namespace) -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    baseline = _bundle_one(SPEC_DIR / "openapi.yaml", DIST / "openapi.bundle.yaml")
    frontier = _bundle_one(SPEC_DIR / "openapi-3.2.yaml", DIST / "openapi-3.2.bundle.yaml")
    _print_ok("bundle baseline", f"{len(operation_ledger(baseline))} operations/events")
    _print_ok("bundle frontier", f"{len(operation_ledger(frontier))} operations/events")


def cmd_bundle_check(_: argparse.Namespace) -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    entry = SPEC_DIR / "openapi.yaml"
    first = bundle_document(entry)
    first_bytes = json.dumps(first, sort_keys=True, separators=(",", ":")).encode()
    second = bundle_document(entry)
    second_bytes = json.dumps(second, sort_keys=True, separators=(",", ":")).encode()
    _BUNDLE_CACHE[entry.resolve()] = copy.deepcopy(first)
    errors: list[str] = []
    if first_bytes != second_bytes:
        errors.append("two bundles from the same source differ")
    source_ledger = operation_ledger(first)
    disk_path = DIST / "openapi.bundle.yaml"
    write_yaml(disk_path, first)
    disk_ledger = operation_ledger(load_yaml(disk_path))
    if source_ledger != disk_ledger:
        errors.append("operation ledger changed during serialization")
    if any("$ref" in json.dumps(row) for row in first.get("paths", {}).values()):
        errors.append("external references remain in bundled paths")
    ensure_no_errors("deterministic bundle", errors)
    digest = hashlib.sha256(disk_path.read_bytes()).hexdigest()
    (DIST / "openapi.bundle.sha256").write_text(f"{digest}  openapi.bundle.yaml\n", encoding="utf-8")
    _print_ok("deterministic bundle", digest[:16])


def cmd_operations(_: argparse.Namespace) -> None:
    spec = _bundled(SPEC_DIR / "openapi.yaml")
    rows = operation_ledger(spec)
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "operation-ledger.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )
    lines = ["# Operation ledger", "", "| Method | Location | operationId |", "|---|---|---|"]
    lines.extend(
        f"| `{row['method']}` | `{row['path']}` | `{row['operationId']}` |" for row in rows
    )
    (DIST / "operation-ledger.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    _print_ok("operation ledger", f"{len(rows)} rows")


def cmd_examples(_: argparse.Namespace) -> None:
    for frontier, version in ((False, "3.1.2"), (True, "3.2.0")):
        spec = _bundled(_entry(frontier))
        ensure_no_errors(f"OpenAPI {version} examples", validate_examples(spec))
        _print_ok("examples", version)


def cmd_fixtures(_: argparse.Namespace) -> None:
    spec = _bundled(SPEC_DIR / "openapi.yaml")
    count, errors = validate_fixture_manifest(
        spec, ROOT / "tests/fixtures/schema/manifest.yaml"
    )
    ensure_no_errors("schema fixtures", errors)
    if count < 40:
        raise CourseValidationError(f"schema fixture corpus is too small: {count}; expected at least 40")
    _print_ok("schema fixture corpus", f"{count} cases")


def cmd_overlays(_: argparse.Namespace) -> None:
    source = _bundled(SPEC_DIR / "openapi.yaml")
    DIST.mkdir(parents=True, exist_ok=True)
    for name in ("public", "partner"):
        overlay_path = SPEC_DIR / "overlays" / f"{name}.overlay.yaml"
        overlay = load_yaml(overlay_path)
        ensure_no_errors(f"{name} overlay", validate_overlay(overlay))
        result = apply_overlay(source, overlay)
        output = DIST / f"openapi.{name}.yaml"
        write_yaml(output, result)
        errors: list[str] = []
        if "/internal/diagnostics" in result.get("paths", {}):
            errors.append("internal diagnostics survived derived view")
        if name == "partner" and "delete" in result.get("paths", {}).get("/datasets/{datasetId}", {}):
            errors.append("dataset deletion survived the partner view")
        ensure_no_errors(f"{name} overlay assertions", errors)
        _print_ok("overlay", name)


def cmd_workflow(_: argparse.Namespace) -> None:
    openapi_spec = _bundled(SPEC_DIR / "openapi.yaml")
    workflow_path = SPEC_DIR / "workflows" / "analysis-run.arazzo.yaml"
    workflow = load_yaml(workflow_path)
    ensure_no_errors("Arazzo workflow", validate_arazzo(workflow, openapi_spec))
    source_url = workflow["sourceDescriptions"][0]["url"]
    source_path = (workflow_path.parent / source_url).resolve()
    expected = (SPEC_DIR / "dist/openapi.bundle.yaml").resolve()
    if source_path != expected:
        raise CourseValidationError(
            f"workflow source resolves to {source_path}; expected {expected}"
        )
    _print_ok("Arazzo workflow", workflow["workflows"][0]["workflowId"])


def _markdown_link_errors() -> list[str]:
    errors: list[str] = []
    link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for path in sorted(COURSE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        # Links shown inside fenced code are examples, not navigation targets.
        text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.DOTALL)
        for raw in link_pattern.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(COURSE)}: missing link target {target!r}"
                )
    return errors


def cmd_markdown(_: argparse.Namespace) -> None:
    ensure_no_errors("Markdown links", _markdown_link_errors())
    _print_ok("Markdown links")


def _extract_operation_ids(path: Path, pattern: str) -> set[str]:
    if not path.exists():
        return set()
    return set(re.findall(pattern, path.read_text(encoding="utf-8")))


def cmd_handler_map(_: argparse.Namespace) -> None:
    spec = _bundled(SPEC_DIR / "openapi.yaml")
    expected = {
        row["operationId"]
        for row in operation_ledger(spec, include_events=False)
        if row["operationId"]
    }
    python_ids: set[str] = set()
    for path in (ROOT / "services/python-fastapi/src").rglob("*.py"):
        python_ids |= _extract_operation_ids(path, r'operation_id\s*=\s*["\']([^"\']+)')
    ts_ids: set[str] = set()
    for path in (ROOT / "services/typescript-fastify/src").rglob("*.ts"):
        ts_ids |= _extract_operation_ids(path, r'operationId\s*:\s*["\']([^"\']+)')
    errors: list[str] = []
    for label, actual in (("Python", python_ids), ("TypeScript", ts_ids)):
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            errors.append(f"{label} handlers missing: {missing}")
        if extra:
            errors.append(f"{label} handlers not in contract: {extra}")
    ensure_no_errors("provider handler map", errors)
    _print_ok("provider handler map", f"{len(expected)} path operations in each provider")


def cmd_releases(_: argparse.Namespace) -> None:
    release_root = ROOT / "releases"
    old = load_yaml(release_root / "v1.0/openapi.yaml")
    new = load_yaml(release_root / "v1.1/openapi.yaml")
    attempted = load_yaml(release_root / "attempted-v1.2-breaking/openapi.yaml")
    major = load_yaml(release_root / "v2.0/openapi.yaml")
    normal = compare_contracts(old, new)
    blocked = compare_contracts(new, attempted)
    major_diff = compare_contracts(new, major)
    errors: list[str] = []
    if not normal["compatible"]:
        errors.append(f"v1.0 -> v1.1 unexpectedly breaking: {normal['breaking']}")
    if blocked["compatible"]:
        errors.append("attempted v1.2 fixture did not contain a detected breaking change")
    if major_diff["compatible"]:
        errors.append("v2.0 fixture did not contain a detected breaking change")
    ensure_no_errors("release fixtures", errors)
    REPORTS.mkdir(parents=True, exist_ok=True)
    report = {"v1.0-to-v1.1": normal, "v1.1-to-attempted-v1.2": blocked, "v1.1-to-v2.0": major_diff}
    (REPORTS / "compatibility.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    _print_ok("release compatibility fixtures", f"{len(blocked['breaking'])} blocked changes")


def _run_subprocess(label: str, command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "label": label,
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
        "passed": completed.returncode == 0,
    }


def _resolve_tool(candidates: list[Path | str]) -> str | None:
    for candidate in candidates:
        value = str(candidate)
        if Path(value).is_absolute():
            if Path(value).is_file() and Path(value).stat().st_mode & 0o111:
                return value
            continue
        resolved = shutil.which(value)
        if resolved:
            return resolved
    return None


def cmd_capability_report(_: argparse.Namespace) -> None:
    node_bin = COURSE / "node_modules" / ".bin"
    venv_bin = COURSE / ".venv" / "bin"
    tools_bin = COURSE / ".tools" / "bin"
    tools: dict[str, dict[str, Any]] = {
        "redocly": {
            "candidates": [node_bin / "redocly", "redocly"],
            "version_args": ["--version"],
            "proof_target": "lint-contract",
        },
        "spectral": {
            "candidates": [node_bin / "spectral", "spectral"],
            "version_args": ["--version"],
            "proof_target": "lint-contract",
        },
        "prism": {
            "candidates": [node_bin / "prism", "prism"],
            "version_args": ["--version"],
            "proof_target": "prism-smoke",
        },
        "openapi-typescript": {
            "candidates": [node_bin / "openapi-typescript", "openapi-typescript"],
            "version_args": ["--version"],
            "proof_target": "clients-generate",
        },
        "schemathesis": {
            "candidates": [venv_bin / "st", venv_bin / "schemathesis", "st", "schemathesis"],
            "version_args": ["--version"],
            "proof_target": "schemathesis",
        },
        "openapi-python-client": {
            "candidates": [venv_bin / "openapi-python-client", "openapi-python-client"],
            "version_args": ["--version"],
            "proof_target": "clients-generate",
        },
        "oasdiff": {
            "candidates": [tools_bin / "oasdiff", "oasdiff"],
            "version_args": ["--version"],
            "proof_target": "oasdiff",
        },
    }
    results: list[dict[str, Any]] = []
    for name, config in tools.items():
        executable = _resolve_tool(config["candidates"])
        if executable is None:
            results.append(
                {
                    "tool": name,
                    "installed": False,
                    "classification": "not-executed",
                    "reason": "pinned executable is not installed",
                    "proofTarget": config["proof_target"],
                }
            )
            continue
        probe = _run_subprocess(name, [executable, *config["version_args"]], COURSE)
        results.append(
            {
                "tool": name,
                "installed": True,
                "classification": "installed" if probe["passed"] else "probe-failed",
                "proofTarget": config["proof_target"],
                **probe,
            }
        )
    REPORTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "baseline": "OpenAPI 3.1.2",
        "frontier": "OpenAPI 3.2.0",
        "results": results,
        "interpretation": {
            "installed": "the pinned executable answered a version probe; no feature support is inferred",
            "probe-failed": "an executable was found but its version probe failed",
            "not-executed": "the executable was absent; this is not evidence of unsupported semantics",
        },
        "nextStep": (
            "Run each proofTarget after make setup. Feature-level results belong in the Module 10 "
            "capability matrix; command availability alone never establishes support."
        ),
    }
    (REPORTS / "tool-capability.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    installed = sum(bool(item.get("installed")) and item["classification"] == "installed" for item in results)
    _print_ok("tool capability inventory", f"{installed}/{len(results)} pinned executables installed")


LOCAL_STEPS = [
    ("structure", cmd_structure),
    ("parse", cmd_parse),
    ("refs", cmd_refs),
    ("bundle", cmd_bundle),
    ("bundle-check", cmd_bundle_check),
    ("operations", cmd_operations),
    ("examples", cmd_examples),
    ("fixtures", cmd_fixtures),
    ("handler-map", cmd_handler_map),
    ("overlays", cmd_overlays),
    ("workflow", cmd_workflow),
    ("releases", cmd_releases),
    ("markdown", cmd_markdown),
]


def cmd_core_proof(args: argparse.Namespace) -> None:
    """Run all dependency-light gates in one process so bundles are reused."""
    for _, function in LOCAL_STEPS:
        function(args)
    _print_ok("Course 1 core proof", f"{len(LOCAL_STEPS)} gates")


def cmd_confirm(args: argparse.Namespace) -> None:
    cmd_core_proof(args)
    _print_ok("local capstone confirmation", f"{len(LOCAL_STEPS)} gates")


def cmd_verify_report(args: argparse.Namespace) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for label, function in LOCAL_STEPS:
        try:
            function(args)
            results.append({"gate": label, "passed": True})
        except Exception as exc:
            results.append({"gate": label, "passed": False, "error": str(exc)})
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "passed": all(item["passed"] for item in results),
        "results": results,
    }
    output = REPORTS / "local-verification.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if not payload["passed"]:
        raise CourseValidationError(f"one or more gates failed; inspect {output}")
    _print_ok("local verification report", str(output.relative_to(ROOT)))


COMMANDS = {
    "structure": cmd_structure,
    "parse": cmd_parse,
    "refs": cmd_refs,
    "bundle": cmd_bundle,
    "bundle-check": cmd_bundle_check,
    "operations": cmd_operations,
    "examples": cmd_examples,
    "fixtures": cmd_fixtures,
    "overlays": cmd_overlays,
    "workflow": cmd_workflow,
    "markdown": cmd_markdown,
    "handler-map": cmd_handler_map,
    "releases": cmd_releases,
    "capability-report": cmd_capability_report,
    "core-proof": cmd_core_proof,
    "confirm": cmd_confirm,
    "verify-report": cmd_verify_report,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenAPI Contract Engineering deterministic gates")
    parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args()
    try:
        COMMANDS[args.command](args)
    except CourseValidationError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
