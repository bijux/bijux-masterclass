from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE_ROOT / "scripts" / "audit_discovery_integrity.py"
SPECIMENS = CAPSTONE_ROOT / "repro" / "discovery-integrity"
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
    return result, json.loads(output.read_text(encoding="utf-8"))


def case(payload: dict[str, object], model: str) -> dict[str, object]:
    cases = payload["cases"]
    assert isinstance(cases, list)
    return next(item for item in cases if item["model"] == model)


def replace(path: Path, old: str, new: str) -> None:
    source = path.read_text(encoding="utf-8")
    assert old in source
    path.write_text(source.replace(old, new), encoding="utf-8")


def test_audit_distinguishes_declared_invalidation_from_ambient_scanning(
    tmp_path: Path,
) -> None:
    result, payload = run_audit(tmp_path)

    assert result.returncode == 0
    assert payload["schema"] == "deep-dive-snakemake-discovery-integrity-audit"
    assert [(item["model"], item["result"], item["finding"]) for item in payload["cases"]] == [
        (
            "governed-registry",
            "PASS",
            "DECLARED_DISCOVERY_INVALIDATION_PRESERVED",
        ),
        (
            "ambient-scan",
            "PASS",
            "AMBIENT_DISCOVERY_STALENESS_REPRODUCED",
        ),
    ]


def test_audit_rejects_a_registry_that_is_not_a_checkpoint_input(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    snakefile = tmp_path / "specimens" / "governed-registry" / "Snakefile"
    replace(
        snakefile,
        '    input:\n        registry="data/arrivals.tsv"\n',
        "",
    )
    replace(
        snakefile,
        "arrivals = Path(input.registry).read_text",
        'arrivals = Path("data/arrivals.tsv").read_text',
    )

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    failures = case(payload, "governed-registry")["failures"]
    assert "checkpoint declares registry input" in failures
    assert "registry change schedules discovery" in failures


def test_audit_rejects_an_ambient_scan_that_cannot_reveal_new_arrivals(
    tmp_path: Path,
) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    snakefile = tmp_path / "specimens" / "ambient-scan" / "Snakefile"
    replace(
        snakefile,
        'samples = sorted(path.stem for path in raw_dir.glob("*.fastq"))',
        'samples = ["alpha"]',
    )

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    failures = case(payload, "ambient-scan")["failures"]
    assert "forced reevaluation reveals hidden arrivals" in failures
