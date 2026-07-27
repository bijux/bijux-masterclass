from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def capstone_root() -> Path:
    return Path(__file__).resolve().parents[1]


def specimen_copy(tmp_path: Path) -> Path:
    destination = tmp_path / "specimen"
    shutil.copytree(capstone_root() / "repro" / "stage-contracts", destination)
    return destination


def replace(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    assert old in content
    path.write_text(content.replace(old, new, 1), encoding="utf-8")


def run_audit(
    tmp_path: Path,
    specimen: Path,
    *,
    check: bool,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    output = tmp_path / "audit" / "report.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(capstone_root() / "scripts" / "audit_stage_contracts.py"),
            "--specimen",
            str(specimen),
            "--workspace",
            str(tmp_path / "audit" / "workspace"),
            "--output",
            str(output),
            "--python",
            sys.executable,
        ],
        check=check,
        text=True,
        capture_output=True,
    )
    return completed, json.loads(output.read_text(encoding="utf-8"))


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


def test_audit_classifies_declared_and_hidden_contracts(tmp_path: Path) -> None:
    _, report = run_audit(tmp_path, specimen_copy(tmp_path), check=True)

    assert [item["decision"] for item in report["findings"]] == [
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "REJECT",
        "ACCEPT",
        "ACCEPT",
        "REJECT",
        "REJECT",
    ]
    assert all(item["result"] == "PASS" for item in report["findings"])


def test_audit_replaces_stale_workspace_evidence(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    run_audit(tmp_path, specimen, check=True)
    stale = tmp_path / "audit" / "workspace" / "stale-evidence.txt"
    stale.write_text("must disappear\n", encoding="utf-8")

    run_audit(tmp_path, specimen, check=True)

    assert not stale.exists()


def test_declared_file_influence_must_be_a_dependency(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    replace(
        specimen / "dvc.yaml",
        "      - policy/threshold.txt\n      - scripts/render.py",
        "      - scripts/render.py",
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "DECLARED_INPUT_CHANGE_IS_STALE")["checks"]
    assert checks["declared_stage_is_stale"] is False


def test_hidden_file_influence_must_remain_undeclared(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    replace(
        specimen / "dvc.yaml",
        (
            "  hidden_input:\n"
            "    cmd: >-\n"
            "      python scripts/render.py input\n"
            "      --source data/source.txt\n"
            "      --policy policy/threshold.txt\n"
            "      --output results/hidden-input.txt\n"
            "    deps:\n"
            "      - data/source.txt\n"
            "      - scripts/render.py"
        ),
        (
            "  hidden_input:\n"
            "    cmd: >-\n"
            "      python scripts/render.py input\n"
            "      --source data/source.txt\n"
            "      --policy policy/threshold.txt\n"
            "      --output results/hidden-input.txt\n"
            "    deps:\n"
            "      - data/source.txt\n"
            "      - policy/threshold.txt\n"
            "      - scripts/render.py"
        ),
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "HIDDEN_INPUT_CHANGE_IS_INVISIBLE")["checks"]
    assert checks["hidden_stage_is_absent_from_status"] is False


def test_declared_control_must_be_a_parameter(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    replace(
        specimen / "dvc.yaml",
        "    params:\n      - settings.multiplier\n    outs:",
        "    outs:",
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "DECLARED_PARAM_CHANGE_IS_STALE")["checks"]
    assert checks["declared_stage_is_stale"] is False


def test_hidden_control_must_remain_undeclared(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    replace(
        specimen / "dvc.yaml",
        (
            "  hidden_param:\n"
            "    cmd: >-\n"
            "      python scripts/render.py param\n"
            "      --source data/source.txt\n"
            "      --params params.yaml\n"
            "      --output results/hidden-param.txt\n"
            "    deps:\n"
            "      - data/source.txt\n"
            "      - scripts/render.py\n"
            "    outs:"
        ),
        (
            "  hidden_param:\n"
            "    cmd: >-\n"
            "      python scripts/render.py param\n"
            "      --source data/source.txt\n"
            "      --params params.yaml\n"
            "      --output results/hidden-param.txt\n"
            "    deps:\n"
            "      - data/source.txt\n"
            "      - scripts/render.py\n"
            "    params:\n"
            "      - settings.multiplier\n"
            "    outs:"
        ),
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "HIDDEN_PARAM_CHANGE_IS_INVISIBLE")["checks"]
    assert checks["hidden_stage_is_absent_from_status"] is False


def test_meaningful_sidecar_must_remain_outside_outputs(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    replace(
        specimen / "dvc.yaml",
        "    outs:\n      - results/declared-main.txt",
        (
            "    outs:\n"
            "      - results/declared-main.txt\n"
            "      - results/undeclared-receipt.txt"
        ),
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "UNDECLARED_OUTPUT_LOSS_IS_INVISIBLE")["checks"]
    assert checks["stage_is_absent_from_status"] is False
    assert checks["lost_sidecar_is_not_restored"] is False


def test_declared_rebuild_must_adopt_file_value(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    replace(
        specimen / "scripts" / "render.py",
        'threshold = args.policy.read_text(encoding="utf-8").strip()',
        'threshold = "10"',
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "DECLARED_INPUT_REBUILDS_CURRENT_VALUE")["checks"]
    assert checks["declared_output_records_current_value"] is False


def test_declared_rebuild_must_adopt_parameter_value(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    replace(
        specimen / "scripts" / "render.py",
        "factor = multiplier(args.params)",
        "factor = 2",
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "DECLARED_PARAM_REBUILDS_CURRENT_VALUE")["checks"]
    assert checks["declared_output_records_current_value"] is False
