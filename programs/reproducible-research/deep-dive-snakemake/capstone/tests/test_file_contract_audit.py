from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def source_root() -> Path:
    return Path(__file__).resolve().parents[1]


def specimen_copy(tmp_path: Path) -> Path:
    destination = tmp_path / "specimen"
    shutil.copytree(source_root() / "repro" / "file-contracts", destination)
    return destination


def script_copy(tmp_path: Path, name: str) -> Path:
    destination = tmp_path / name
    shutil.copy2(source_root() / "scripts" / name, destination)
    return destination


def snakemake_binary() -> str:
    discovered = shutil.which("snakemake")
    if discovered is not None:
        return discovered
    environment_binary = Path(sys.executable).with_name("snakemake")
    if environment_binary.is_file():
        return str(environment_binary)
    raise RuntimeError(
        "snakemake must be on PATH or installed beside the active Python interpreter"
    )


def run_audit(
    tmp_path: Path,
    specimen: Path,
    *,
    poison_writer: Path | None = None,
    atomic_writer: Path | None = None,
    check: bool,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    output = tmp_path / "audit" / "report.json"
    command = [
        sys.executable,
        str(source_root() / "scripts" / "audit_file_contracts.py"),
        "--specimen",
        str(specimen),
        "--workspace",
        str(tmp_path / "audit" / "workspace"),
        "--output",
        str(output),
        "--snakemake",
        snakemake_binary(),
        "--python",
        sys.executable,
        "--poison-writer",
        str(poison_writer or source_root() / "scripts" / "poison.py"),
        "--atomic-writer",
        str(atomic_writer or source_root() / "scripts" / "atomic_writer.py"),
    ]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=check,
    )
    return completed, json.loads(output.read_text(encoding="utf-8"))


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


def replace(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    assert old in content
    path.write_text(content.replace(old, new, 1), encoding="utf-8")


def test_audit_classifies_convergence_hidden_inputs_and_publication(
    tmp_path: Path,
) -> None:
    _, report = run_audit(tmp_path, specimen_copy(tmp_path), check=True)

    assert [item["decision"] for item in report["findings"]] == [
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "REJECT",
        "REJECT",
        "ACCEPT",
        "ACCEPT",
    ]
    assert all(item["result"] == "PASS" for item in report["findings"])


def test_audit_replaces_stale_workspace_evidence(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    run_audit(tmp_path, specimen, check=True)
    stale = tmp_path / "audit" / "workspace" / "stale-evidence.txt"
    stale.write_text("must disappear\n", encoding="utf-8")

    run_audit(tmp_path, specimen, check=True)

    assert not stale.exists()


def test_declared_policy_must_be_an_input(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    snakefile = specimen / "Snakefile"
    replace(
        snakefile,
        '        policy="policy/threshold.txt",\n    output:',
        '    params:\n        policy="policy/threshold.txt",\n    output:',
    )
    replace(snakefile, "--policy {input.policy:q}", "--policy {params.policy:q}")

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "DECLARED_POLICY_CHANGE_PLANS_RERUN")["checks"]
    assert checks["declared_rule_planned"] is False


def test_declared_rebuild_must_adopt_the_current_policy(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    renderer = specimen / "scripts" / "render_report.py"
    replace(
        renderer,
        'threshold = args.policy.read_text(encoding="utf-8").strip()',
        'threshold = "10"',
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "DECLARED_POLICY_CHANGE_REBUILDS_CURRENT_VALUE")["checks"]
    assert checks["declared_output_records_current_value"] is False


def test_hidden_policy_case_must_miss_the_rerun(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    snakefile = specimen / "Snakefile"
    replace(
        snakefile,
        'rule hidden_report:\n    input:\n        source="data/source.txt",\n',
        (
            'rule hidden_report:\n    input:\n        source="data/source.txt",\n'
            '        policy="policy/threshold.txt",\n'
        ),
    )
    replace(
        snakefile,
        '    params:\n        policy="policy/threshold.txt",\n',
        "",
    )
    replace(snakefile, "--policy {params.policy:q}", "--policy {input.policy:q}")

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "HIDDEN_POLICY_CHANGE_MISSES_RERUN")["checks"]
    assert checks["hidden_dry_run_has_no_jobs"] is False


def test_in_place_failure_must_reach_the_final_path(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    poison = script_copy(tmp_path, "poison.py")
    replace(
        poison,
        'output.write_text("PARTIAL\\n", encoding="utf-8")',
        'output.with_suffix(".scratch").write_text("PARTIAL\\n", encoding="utf-8")',
    )

    completed, report = run_audit(
        tmp_path,
        specimen,
        poison_writer=poison,
        check=False,
    )

    assert completed.returncode != 0
    checks = finding(report, "IN_PLACE_FAILURE_POISONS_FINAL")["checks"]
    assert checks["trusted_final_was_replaced"] is False


def test_atomic_failure_must_preserve_the_final_path(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    atomic = script_copy(tmp_path, "atomic_writer.py")
    replace(
        atomic,
        'if args.fail_before_rename:\n        print("Crashing before rename.", file=sys.stderr)',
        (
            "if args.fail_before_rename:\n"
            '        final_output.write_text("PARTIAL\\n", encoding="utf-8")\n'
            '        print("Crashing before rename.", file=sys.stderr)'
        ),
    )

    completed, report = run_audit(
        tmp_path,
        specimen,
        atomic_writer=atomic,
        check=False,
    )

    assert completed.returncode != 0
    checks = finding(report, "ATOMIC_FAILURE_PRESERVES_FINAL")["checks"]
    assert checks["trusted_final_survived"] is False


def test_atomic_success_must_promote_scratch(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    atomic = script_copy(tmp_path, "atomic_writer.py")
    replace(
        atomic,
        "temp_output.replace(final_output)",
        'final_output.write_text("complete\\n", encoding="utf-8")',
    )

    completed, report = run_audit(
        tmp_path,
        specimen,
        atomic_writer=atomic,
        check=False,
    )

    assert completed.returncode != 0
    checks = finding(report, "ATOMIC_SUCCESS_PROMOTES_COMPLETE_OUTPUT")["checks"]
    assert checks["scratch_was_promoted"] is False
