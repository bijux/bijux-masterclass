from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE_ROOT / "scripts" / "audit_module_interfaces.py"
SPECIMENS = CAPSTONE_ROOT / "repro" / "module-interfaces"
SNAKEMAKE = Path(sys.executable).with_name("snakemake")


def run_audit(tmp_path: Path) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    specimens = tmp_path / "specimens"
    if not specimens.exists():
        shutil.copytree(SPECIMENS, specimens)
    output = tmp_path / "report" / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--specimens",
            str(specimens),
            "--workspace",
            str(tmp_path / "workspace"),
            "--output",
            str(output),
            "--snakemake",
            str(SNAKEMAKE),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    payload = json.loads(output.read_text(encoding="utf-8"))
    return result, payload


def case(payload: dict[str, object], model: str) -> dict[str, object]:
    cases = payload["cases"]
    assert isinstance(cases, list)
    return next(item for item in cases if item["model"] == model)


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")


def test_capstone_modules_receive_only_declared_runtime_config() -> None:
    caller = (CAPSTONE_ROOT / "workflow" / "rules" / "preprocess.smk").read_text(encoding="utf-8")
    assert caller.count("config: MODULE_RUNTIME_CONFIG") == 2
    assert "config: config\n" not in caller

    for module_path in (
        CAPSTONE_ROOT / "workflow" / "modules" / "qc_module" / "Snakefile",
        CAPSTONE_ROOT / "workflow" / "modules" / "screen_module" / "Snakefile",
    ):
        module_source = module_path.read_text(encoding="utf-8")
        config_keys = set(re.findall(r'config\["([^"]+)"\]', module_source))
        assert config_keys == {"env_python", "benchmarks_dir"}


def test_audit_distinguishes_explicit_contract_from_hidden_coupling(tmp_path: Path) -> None:
    result, payload = run_audit(tmp_path)

    assert result.returncode == 0
    assert payload["schema"] == "deep-dive-snakemake-module-interface-audit"
    assert [(item["model"], item["result"], item["finding"]) for item in payload["cases"]] == [
        (
            "explicit-contract",
            "PASS",
            "EXPLICIT_MODULE_CONTRACT_PRESERVED",
        ),
        (
            "hidden-coupling",
            "PASS",
            "HIDDEN_MODULE_COUPLING_REPRODUCED",
        ),
    ]


def test_audit_replaces_stale_workspace_before_execution(tmp_path: Path) -> None:
    stale = tmp_path / "workspace" / "explicit-contract" / "build"
    stale.mkdir(parents=True)
    (stale / "sample.txt").write_text("stale\n", encoding="utf-8")

    result, payload = run_audit(tmp_path)

    assert result.returncode == 0
    observations = case(payload, "explicit-contract")["observations"]
    assert observations["artifact_lines"] == ["reviewed", "sample payload"]


def test_audit_rejects_broad_config_in_explicit_contract(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    snakefile = tmp_path / "specimens" / "explicit-contract" / "Snakefile"
    replace(snakefile, 'config: config["normalize"]', "config: config")

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    assert "module receives narrow config" in case(payload, "explicit-contract")["failures"]


def test_audit_rejects_missing_policy_binding_in_explicit_contract(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    snakefile = tmp_path / "specimens" / "explicit-contract" / "Snakefile"
    replace(snakefile, 'prefix=config["normalize"]["prefix"]', 'prefix="reviewed"')

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    assert "caller binds policy" in case(payload, "explicit-contract")["failures"]


def test_audit_rejects_missing_output_binding_in_explicit_contract(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    snakefile = tmp_path / "specimens" / "explicit-contract" / "Snakefile"
    replace(snakefile, 'artifact="build/sample.txt"', 'artifact="build/renamed.txt"')

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    assert "caller binds output" in case(payload, "explicit-contract")["failures"]


def test_audit_rejects_exposed_policy_in_hidden_coupling_model(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    snakefile = tmp_path / "specimens" / "hidden-coupling" / "Snakefile"
    replace(
        snakefile,
        '        artifact="build/sample.txt"\n',
        '        artifact="build/sample.txt"\n'
        "    params:\n"
        '        prefix=config["private"]["prefix"]\n',
    )

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    assert "caller leaves policy hidden" in case(payload, "hidden-coupling")["failures"]


def test_audit_rejects_removed_private_read_in_hidden_coupling_model(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    snakefile = tmp_path / "specimens" / "hidden-coupling" / "module" / "Snakefile"
    replace(snakefile, 'prefix=config["private"]["prefix"]', 'prefix="inherited"')

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    assert "module reads private policy" in case(payload, "hidden-coupling")["failures"]
