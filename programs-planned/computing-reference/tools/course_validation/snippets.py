from __future__ import annotations

import ast
import json
import os
import platform
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .manifest import find_module
from .result import ValidationResult

try:
    import resource
except ImportError:  # pragma: no cover - resource is unavailable on Windows
    resource = None

ANNOTATION = re.compile(r"^<!--\s*bijux-verify:\s*(\{.*\})\s*-->\s*$")
FENCE_START = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
SNIPPET_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

SAFE_PYTHON_IMPORTS = {
    "bisect",
    "collections",
    "dataclasses",
    "decimal",
    "enum",
    "fractions",
    "functools",
    "hashlib",
    "heapq",
    "itertools",
    "math",
    "operator",
    "random",
    "re",
    "statistics",
    "string",
    "typing",
}

DENIED_PYTHON_CALLS = {
    "__import__",
    "breakpoint",
    "compile",
    "delattr",
    "eval",
    "exec",
    "getattr",
    "globals",
    "input",
    "locals",
    "open",
    "setattr",
    "vars",
}

DENIED_PYTHON_ATTRIBUTES = {
    "chmod",
    "connect",
    "dump",
    "dumps",
    "exec",
    "execv",
    "execve",
    "fork",
    "kill",
    "mkdir",
    "open",
    "popen",
    "remove",
    "rename",
    "replace",
    "rmdir",
    "send",
    "socket",
    "spawn",
    "system",
    "touch",
    "unlink",
    "write_bytes",
    "write_text",
}

LANGUAGE_SUFFIXES = {
    "python": ".py",
}

EXECUTION_REGISTRY = {
    ("python", "python3"),
}

MAX_OUTPUT_BYTES = 1_048_576

LANGUAGE_ALIASES = {
    "py": "python",
    "python": "python",
    "python3": "python",
}


@dataclass(frozen=True)
class Snippet:
    identifier: str
    mode: str
    language: str
    toolchain: str
    code: str
    line: int
    expect: dict[str, Any] | None = None
    reason: str | None = None


@dataclass(frozen=True)
class SnippetReport:
    module_id: str
    entries: tuple[dict[str, Any], ...]
    issues: tuple[str, ...] = ()

    @property
    def counts(self) -> dict[str, int]:
        counts = {"passed": 0, "failed": 0, "skipped": 0, "unavailable": 0}
        for entry in self.entries:
            counts[entry["status"]] += 1
        return counts

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "module_id": self.module_id,
            "validation_status": "failed" if self.issues else "passed",
            "environment": {
                "operating_system": platform.platform(),
                "python_implementation": platform.python_implementation(),
            },
            "summary": self.counts,
            "issues": list(self.issues),
            "limitations": (
                "Execution establishes observed local behavior only. Static safety checks, "
                "a five-second timeout, and available POSIX resource limits constrain but do "
                "not prove universal safety or correctness."
            ),
            "entries": list(self.entries),
        }


def _canonical_language(language: str) -> str:
    normalized = language.casefold().strip()
    return LANGUAGE_ALIASES.get(normalized, normalized)


def _parse_annotation(
    raw: str,
    fence_language: str,
    line: int,
    issues: list[str],
) -> Snippet | None:
    try:
        annotation = json.loads(raw)
    except json.JSONDecodeError as error:
        issues.append(f"line {line}: invalid bijux-verify JSON: {error.msg}")
        return None
    if not isinstance(annotation, dict):
        issues.append(f"line {line}: bijux-verify annotation must be a JSON object")
        return None

    mode = annotation.get("mode")
    required = {"id", "mode", "language", "toolchain"}
    if mode in {"run", "compile"}:
        required.add("expect")
    elif mode in {"schematic", "data"}:
        required.add("reason")
    else:
        issues.append(f"line {line}: unsupported snippet mode {mode!r}")
        return None
    if set(annotation) != required:
        issues.append(
            f"line {line}: annotation fields must be exactly {', '.join(sorted(required))}"
        )
        return None

    identifier = annotation["id"]
    language = annotation["language"]
    toolchain = annotation["toolchain"]
    if not isinstance(identifier, str) or not SNIPPET_ID.fullmatch(identifier):
        issues.append(f"line {line}: invalid snippet id {identifier!r}")
        return None
    if not isinstance(language, str) or not language.strip():
        issues.append(f"line {line}: snippet language must be a nonempty string")
        return None
    if not isinstance(toolchain, str) or not toolchain.strip():
        issues.append(f"line {line}: snippet toolchain must be a nonempty string")
        return None
    language = _canonical_language(language)
    if _canonical_language(fence_language) != language:
        issues.append(f"line {line}: annotation language differs from the code fence")
        return None

    expect = annotation.get("expect")
    reason = annotation.get("reason")
    if mode in {"run", "compile"}:
        if toolchain == "none":
            issues.append(f"line {line}: executable snippets require a toolchain")
            return None
        if not isinstance(expect, dict) or not expect:
            issues.append(f"line {line}: executable snippets require a nonempty expect object")
            return None
        allowed_expectations = {
            "exit_code",
            "stdout",
            "stderr",
            "stdout_contains",
            "stderr_contains",
        }
        if not set(expect).issubset(allowed_expectations) or "exit_code" not in expect:
            issues.append(f"line {line}: invalid executable expectation fields")
            return None
        if not isinstance(expect["exit_code"], int):
            issues.append(f"line {line}: expected exit_code must be an integer")
            return None
        for field in set(expect) - {"exit_code"}:
            if not isinstance(expect[field], str):
                issues.append(f"line {line}: expected {field} must be a string")
                return None
    else:
        if toolchain != "none":
            issues.append(f"line {line}: non-executable snippets must use toolchain none")
            return None
        if not isinstance(reason, str) or not reason.strip():
            issues.append(f"line {line}: non-executable snippets require a reason")
            return None

    return Snippet(
        identifier=identifier,
        mode=mode,
        language=language,
        toolchain=toolchain,
        code="",
        line=line,
        expect=expect,
        reason=reason,
    )


def parse_snippets(text: str) -> tuple[list[Snippet], ValidationResult]:
    lines = text.splitlines()
    snippets: list[Snippet] = []
    issues: list[str] = []
    annotation_lines: set[int] = set()
    used_annotations: set[int] = set()
    index = 0
    while index < len(lines):
        annotation_match = ANNOTATION.match(lines[index])
        if annotation_match:
            annotation_lines.add(index)
        fence_match = FENCE_START.match(lines[index])
        if not fence_match:
            index += 1
            continue

        fence = fence_match.group("fence")
        marker = fence[0]
        info = fence_match.group("info").strip()
        language = info.split(maxsplit=1)[0] if info else ""
        closing = re.compile(rf"^{re.escape(marker)}{{{len(fence)},}}\s*$")
        end = index + 1
        while end < len(lines) and not closing.match(lines[end]):
            end += 1
        if end == len(lines):
            issues.append(f"line {index + 1}: unclosed code fence")
            break
        if not language:
            issues.append(f"line {index + 1}: code fence must declare a language")

        annotation_index = index - 1
        if annotation_index < 0 or not (match := ANNOTATION.match(lines[annotation_index])):
            issues.append(f"line {index + 1}: code fence lacks an immediate bijux-verify annotation")
        elif language:
            used_annotations.add(annotation_index)
            parsed = _parse_annotation(
                match.group(1),
                language,
                annotation_index + 1,
                issues,
            )
            if parsed is not None:
                snippets.append(
                    Snippet(
                        identifier=parsed.identifier,
                        mode=parsed.mode,
                        language=parsed.language,
                        toolchain=parsed.toolchain,
                        code="\n".join(lines[index + 1:end]) + "\n",
                        line=index + 1,
                        expect=parsed.expect,
                        reason=parsed.reason,
                    )
                )
        index = end + 1

    for annotation_index in sorted(annotation_lines - used_annotations):
        issues.append(f"line {annotation_index + 1}: orphan bijux-verify annotation")
    identifiers = [snippet.identifier for snippet in snippets]
    duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
    if duplicates:
        issues.append(f"duplicate snippet ids: {', '.join(duplicates)}")
    return snippets, ValidationResult(tuple(issues))


def _python_safety(code: str) -> ValidationResult:
    issues: list[str] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return ValidationResult((f"Python syntax error on line {error.lineno}: {error.msg}",))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = {alias.name.split(".", 1)[0] for alias in node.names}
            denied = sorted(names - SAFE_PYTHON_IMPORTS)
            if denied:
                issues.append(f"Python imports are not allowed in verification: {', '.join(denied)}")
        elif isinstance(node, ast.ImportFrom):
            name = (node.module or "").split(".", 1)[0]
            if node.level or name not in SAFE_PYTHON_IMPORTS:
                issues.append(f"Python import is not allowed in verification: {node.module!r}")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in DENIED_PYTHON_CALLS:
                issues.append(f"Python call is not allowed in verification: {node.func.id}")
            if isinstance(node.func, ast.Attribute) and node.func.attr in DENIED_PYTHON_ATTRIBUTES:
                issues.append(f"Python method is not allowed in verification: {node.func.attr}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            issues.append(f"Python dunder access is not allowed in verification: {node.attr}")
    return ValidationResult(tuple(dict.fromkeys(issues)))


def _command_for(snippet: Snippet, source: Path) -> tuple[list[str], ValidationResult]:
    if (snippet.language, snippet.toolchain) not in EXECUTION_REGISTRY:
        return [], ValidationResult(
            (f"unsupported execution route: {snippet.language}/{snippet.toolchain}",)
        )
    if snippet.language == "python":
        safety = _python_safety(snippet.code)
        if not safety.ok:
            return [], safety
        if snippet.mode == "compile":
            return [sys.executable, "-I", "-B", "-m", "py_compile", str(source)], safety
        return [sys.executable, "-I", "-B", str(source)], safety
    return [], ValidationResult((f"no runner owns language {snippet.language}",))


def _toolchain_version(snippet: Snippet) -> tuple[str | None, str | None]:
    if (snippet.language, snippet.toolchain) != ("python", "python3"):
        return None, f"unsupported execution route: {snippet.language}/{snippet.toolchain}"
    try:
        completed = subprocess.run(
            [sys.executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, str(error)
    version = (completed.stdout or completed.stderr).strip()
    if completed.returncode != 0:
        return None, version or f"version command exited {completed.returncode}"
    return version, None


def _expectation_failures(expect: dict[str, Any], completed: subprocess.CompletedProcess[str]) -> list[str]:
    failures: list[str] = []
    if completed.returncode != expect["exit_code"]:
        failures.append(
            f"exit code {completed.returncode} differs from expected {expect['exit_code']}"
        )
    for stream in ("stdout", "stderr"):
        actual = getattr(completed, stream)
        if stream in expect and actual != expect[stream]:
            failures.append(f"{stream} differs from its exact expectation")
        contains = f"{stream}_contains"
        if contains in expect and expect[contains] not in actual:
            failures.append(f"{stream} does not contain the expected text")
    return failures


def _resource_limits() -> None:
    if resource is None:
        return
    limits = (
        (resource.RLIMIT_CPU, 3),
        (resource.RLIMIT_FSIZE, MAX_OUTPUT_BYTES),
        (resource.RLIMIT_NOFILE, 32),
    )
    for resource_kind, requested in limits:
        _, hard = resource.getrlimit(resource_kind)
        maximum = requested if hard == resource.RLIM_INFINITY else min(requested, hard)
        resource.setrlimit(resource_kind, (maximum, maximum))


def _run_command(
    command: list[str],
    directory: Path,
    environment: dict[str, str],
    identifier: str,
) -> subprocess.CompletedProcess[str]:
    stdout_path = directory / f"{identifier}.stdout.txt"
    stderr_path = directory / f"{identifier}.stderr.txt"
    with stdout_path.open("w", encoding="utf-8") as stdout_handle, stderr_path.open(
        "w", encoding="utf-8"
    ) as stderr_handle:
        completed = subprocess.run(
            command,
            cwd=directory,
            env=environment,
            check=False,
            stdout=stdout_handle,
            stderr=stderr_handle,
            timeout=5,
            preexec_fn=_resource_limits if resource is not None else None,
        )
    return subprocess.CompletedProcess(
        command,
        completed.returncode,
        stdout=stdout_path.read_text(encoding="utf-8", errors="replace"),
        stderr=stderr_path.read_text(encoding="utf-8", errors="replace"),
    )


def _write_report(root: Path, report: SnippetReport) -> Path:
    report_directory = root / "artifacts" / "snippets" / report.module_id
    report_directory.mkdir(parents=True, exist_ok=True)
    path = report_directory / "report.json"
    temporary = report_directory / ".report.json.pending"
    temporary.write_text(
        json.dumps(report.as_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
    return path


def verify_snippets(
    root: Path,
    module_id: str,
    text: str,
) -> tuple[ValidationResult, SnippetReport, Path]:
    root = root.resolve()
    if not re.fullmatch(r"[A-Z0-9]+-\d{3}", module_id):
        raise ValueError(f"invalid canonical module ID: {module_id!r}")
    snippets, parse_result = parse_snippets(text)
    issues = list(parse_result.issues)
    entries: list[dict[str, Any]] = []
    module_directory = root / "artifacts" / "snippets" / module_id
    module_directory.mkdir(parents=True, exist_ok=True)
    if issues:
        report = SnippetReport(module_id=module_id, entries=(), issues=tuple(issues))
        report_path = _write_report(root, report)
        return parse_result, report, report_path

    for snippet in snippets:
        base_entry: dict[str, Any] = {
            "id": snippet.identifier,
            "line": snippet.line,
            "mode": snippet.mode,
            "language": snippet.language,
            "toolchain": snippet.toolchain,
            "dependencies": [],
        }
        if snippet.mode in {"schematic", "data"}:
            entries.append({**base_entry, "status": "skipped", "reason": snippet.reason})
            continue

        suffix = LANGUAGE_SUFFIXES.get(snippet.language, ".txt")
        source = module_directory / f"{snippet.identifier}{suffix}"
        source.write_text(snippet.code, encoding="utf-8")
        base_entry["source"] = str(source.relative_to(root))
        if (snippet.language, snippet.toolchain) not in EXECUTION_REGISTRY:
            reason = f"unsupported execution route: {snippet.language}/{snippet.toolchain}"
            issues.append(f"{snippet.identifier}: {reason}")
            entries.append({**base_entry, "status": "unavailable", "reason": reason})
            continue
        command, command_result = _command_for(snippet, source)
        if not command_result.ok:
            reason = "; ".join(command_result.issues)
            issues.append(f"{snippet.identifier}: {reason}")
            entries.append({**base_entry, "status": "failed", "reason": reason})
            continue
        version, unavailable_reason = _toolchain_version(snippet)
        if unavailable_reason:
            issues.append(f"{snippet.identifier}: toolchain unavailable: {unavailable_reason}")
            entries.append(
                {**base_entry, "status": "unavailable", "reason": unavailable_reason}
            )
            continue

        environment = {
            "LC_ALL": "C.UTF-8",
            "PATH": os.environ.get("PATH", ""),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
        }
        try:
            completed = _run_command(
                command,
                module_directory,
                environment,
                snippet.identifier,
            )
        except subprocess.TimeoutExpired as error:
            reason = "execution exceeded the five-second limit"
            issues.append(f"{snippet.identifier}: {reason}")
            entries.append(
                {
                    **base_entry,
                    "status": "failed",
                    "toolchain_version": version,
                    "command": command,
                    "stdout_artifact": str(
                        (module_directory / f"{snippet.identifier}.stdout.txt").relative_to(root)
                    ),
                    "stderr_artifact": str(
                        (module_directory / f"{snippet.identifier}.stderr.txt").relative_to(root)
                    ),
                    "stdout": error.stdout or "",
                    "stderr": error.stderr or "",
                    "reason": reason,
                }
            )
            continue
        failures = _expectation_failures(snippet.expect or {}, completed)
        status = "failed" if failures else "passed"
        if failures:
            issues.append(f"{snippet.identifier}: {'; '.join(failures)}")
        entries.append(
            {
                **base_entry,
                "status": status,
                "toolchain_version": version,
                "command": command,
                "stdout_artifact": str(
                    (module_directory / f"{snippet.identifier}.stdout.txt").relative_to(root)
                ),
                "stderr_artifact": str(
                    (module_directory / f"{snippet.identifier}.stderr.txt").relative_to(root)
                ),
                "expected": snippet.expect,
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                **({"reason": "; ".join(failures)} if failures else {}),
            }
        )

    report = SnippetReport(
        module_id=module_id,
        entries=tuple(entries),
        issues=tuple(issues),
    )
    report_path = _write_report(root, report)
    return ValidationResult(tuple(issues)), report, report_path


def verify_chapter_snippets(
    root: Path,
    module_id: str,
) -> tuple[ValidationResult, SnippetReport | None, Path | None]:
    root = root.resolve()
    row = find_module(root, module_id)
    if row is None:
        return ValidationResult((f"module ID does not resolve exactly once: {module_id}",)), None, None
    chapter = root / row["future_path"]
    if not chapter.is_file():
        return ValidationResult((f"module file is missing: {row['future_path']}",)), None, None
    try:
        text = chapter.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return ValidationResult((f"cannot read module file: {error}",)), None, None
    return verify_snippets(root, module_id, text)
