#!/usr/bin/env python3
"""Prove that execution profiles preserve, or deliberately leak, workflow meaning."""

from __future__ import annotations

import argparse
import csv
import io
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

POLICY_KEYS = {
    "cores",
    "jobs",
    "latency-wait",
    "printshellcmds",
    "rerun-incomplete",
    "show-failed-logs",
}
SEMANTIC_KEYS = {"config", "configfile", "configfiles"}
PRESERVING_PROFILES = ("local", "ci", "scheduler")
LEAK_PROFILES = ("trusted-path-leak", "sample-scope-leak")


@dataclass(frozen=True)
class CommandEvidence:
    argv: list[str]
    returncode: int
    stdout_file: str
    stderr_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--snakemake", type=Path, required=True)
    return parser.parse_args()


def run_command(
    argv: list[str],
    *,
    cwd: Path,
    evidence_dir: Path,
    label: str,
) -> tuple[subprocess.CompletedProcess[str], CommandEvidence]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    stdout_path = evidence_dir / f"{label}.stdout.txt"
    stderr_path = evidence_dir / f"{label}.stderr.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    evidence = CommandEvidence(
        argv=argv,
        returncode=completed.returncode,
        stdout_file=stdout_path.name,
        stderr_file=stderr_path.name,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{label} failed with exit {completed.returncode}; read {stderr_path.as_posix()}"
        )
    return completed, evidence


def load_profile(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"profile must be a mapping: {path}")
    return payload


def classify_profile(payload: dict[str, Any]) -> dict[str, list[str]]:
    keys = set(payload)
    return {
        "policy_keys": sorted(keys & POLICY_KEYS),
        "semantic_keys": sorted(keys & SEMANTIC_KEYS),
        "unknown_keys": sorted(keys - POLICY_KEYS - SEMANTIC_KEYS),
    }


def parse_summary(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    try:
        header_index = next(
            index for index, line in enumerate(lines) if line.startswith("output_file\t")
        )
    except StopIteration as error:
        raise ValueError("Snakemake summary did not contain a TSV header") from error
    reader = csv.DictReader(io.StringIO("\n".join(lines[header_index:])), delimiter="\t")
    return [
        {
            "output_file": row["output_file"],
            "rule": row["rule"],
        }
        for row in reader
    ]


def parse_d3dag(text: str) -> dict[str, Any]:
    for line in reversed(text.splitlines()):
        candidate = line.strip()
        if candidate.startswith('{"nodes":'):
            return json.loads(candidate)
    raise ValueError("Snakemake D3 DAG output did not contain JSON")


def normalize_dag(payload: dict[str, Any]) -> dict[str, Any]:
    nodes_by_id = {
        node["id"]: {
            "label": node["value"]["label"],
            "rule": node["value"]["rule"],
        }
        for node in payload["nodes"]
    }
    nodes = sorted(nodes_by_id.values(), key=lambda node: (node["rule"], node["label"]))
    edges = sorted(
        {
            (
                nodes_by_id[edge["u"]]["label"],
                nodes_by_id[edge["v"]]["label"],
            )
            for edge in payload["edges"]
        }
    )
    return {
        "nodes": nodes,
        "edges": [list(edge) for edge in edges],
    }


def read_artifacts(run_dir: Path, summary: list[dict[str, str]]) -> dict[str, Any]:
    output_paths = sorted(row["output_file"] for row in summary)
    manifest_paths = [path for path in output_paths if path.endswith("/manifest.tsv")]
    if len(manifest_paths) != 1:
        raise ValueError(f"expected one manifest path, found {manifest_paths}")
    manifest_path = manifest_paths[0]
    return {
        "manifest_path": manifest_path,
        "manifest_text": (run_dir / manifest_path).read_text(encoding="utf-8"),
        "normalized_results": {
            path: (run_dir / path).read_text(encoding="utf-8")
            for path in output_paths
            if path.startswith("results/")
        },
    }


def collect_profile(
    *,
    name: str,
    specimen: Path,
    workspace: Path,
    snakemake: Path,
) -> dict[str, Any]:
    run_dir = workspace / "runs" / name
    shutil.copytree(specimen, run_dir)
    evidence_dir = workspace / "evidence" / name
    evidence_dir.mkdir(parents=True, exist_ok=True)
    profile_path = run_dir / "profiles" / name / "config.yaml"
    profile = load_profile(profile_path)
    base_command = [str(snakemake), "--profile", f"profiles/{name}"]

    summary_run, summary_evidence = run_command(
        [*base_command, "--summary"],
        cwd=run_dir,
        evidence_dir=evidence_dir,
        label="summary",
    )
    dag_run, dag_evidence = run_command(
        [*base_command, "--d3dag"],
        cwd=run_dir,
        evidence_dir=evidence_dir,
        label="d3dag",
    )
    dry_run, dry_evidence = run_command(
        [*base_command, "--dry-run", "--printshellcmds"],
        cwd=run_dir,
        evidence_dir=evidence_dir,
        label="dry-run",
    )
    execution, execution_evidence = run_command(
        base_command,
        cwd=run_dir,
        evidence_dir=evidence_dir,
        label="execution",
    )

    summary = parse_summary(summary_run.stdout)
    return {
        "profile": profile,
        "classification": classify_profile(profile),
        "semantic_plan": {
            "outputs": sorted(
                summary,
                key=lambda row: (row["output_file"], row["rule"]),
            ),
            "dag": normalize_dag(parse_d3dag(dag_run.stdout)),
        },
        "artifacts": read_artifacts(run_dir, summary),
        "commands": {
            "summary": asdict(summary_evidence),
            "d3dag": asdict(dag_evidence),
            "dry_run": asdict(dry_evidence),
            "execution": asdict(execution_evidence),
        },
    }


def preserving_finding(profiles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    baseline = profiles["local"]
    comparisons: dict[str, dict[str, bool]] = {}
    for name in PRESERVING_PROFILES:
        current = profiles[name]
        comparisons[name] = {
            "policy_only_profile": not current["classification"]["semantic_keys"]
            and not current["classification"]["unknown_keys"],
            "same_semantic_plan": current["semantic_plan"] == baseline["semantic_plan"],
            "same_manifest_path": current["artifacts"]["manifest_path"]
            == baseline["artifacts"]["manifest_path"],
            "same_manifest_text": current["artifacts"]["manifest_text"]
            == baseline["artifacts"]["manifest_text"],
            "same_results": current["artifacts"]["normalized_results"]
            == baseline["artifacts"]["normalized_results"],
        }
    passed = all(all(checks.values()) for checks in comparisons.values())
    return {
        "finding": "CONTEXT_POLICY_PRESERVED",
        "result": "PASS" if passed else "FAIL",
        "comparisons": comparisons,
    }


def trusted_path_finding(profiles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    baseline = profiles["local"]
    leak = profiles["trusted-path-leak"]
    checks = {
        "semantic_override_visible": leak["classification"]["semantic_keys"] == ["config"],
        "trusted_path_changed": leak["artifacts"]["manifest_path"]
        != baseline["artifacts"]["manifest_path"],
        "sample_results_unchanged": leak["artifacts"]["normalized_results"]
        == baseline["artifacts"]["normalized_results"],
        "manifest_meaning_unchanged": leak["artifacts"]["manifest_text"]
        == baseline["artifacts"]["manifest_text"],
    }
    return {
        "finding": "TRUSTED_PATH_LEAK_REPRODUCED",
        "result": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
    }


def sample_scope_finding(profiles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    baseline = profiles["local"]
    leak = profiles["sample-scope-leak"]
    leak_results = leak["artifacts"]["normalized_results"]
    checks = {
        "semantic_override_visible": leak["classification"]["semantic_keys"] == ["config"],
        "trusted_path_unchanged": leak["artifacts"]["manifest_path"]
        == baseline["artifacts"]["manifest_path"],
        "beta_removed_from_plan": "results/beta.txt" not in leak_results,
        "alpha_preserved": leak_results.get("results/alpha.txt")
        == baseline["artifacts"]["normalized_results"].get("results/alpha.txt"),
        "manifest_changed": leak["artifacts"]["manifest_text"]
        != baseline["artifacts"]["manifest_text"],
    }
    return {
        "finding": "SAMPLE_SCOPE_LEAK_REPRODUCED",
        "result": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
    }


def write_summary(path: Path, findings: list[dict[str, Any]]) -> None:
    rows = ["finding\tresult"]
    rows.extend(f"{item['finding']}\t{item['result']}" for item in findings)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    specimen = args.specimen.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    snakemake = args.snakemake.resolve()

    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    profiles = {
        name: collect_profile(
            name=name,
            specimen=specimen,
            workspace=workspace,
            snakemake=snakemake,
        )
        for name in (*PRESERVING_PROFILES, *LEAK_PROFILES)
    }
    findings = [
        preserving_finding(profiles),
        trusted_path_finding(profiles),
        sample_scope_finding(profiles),
    ]
    report = {
        "schema": "deep-dive-snakemake-context-invariance-audit",
        "profiles": profiles,
        "findings": findings,
    }
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(output.parent / "summary.tsv", findings)

    failed = [finding["finding"] for finding in findings if finding["result"] != "PASS"]
    if failed:
        raise SystemExit(f"FAIL: context-invariance findings failed: {', '.join(failed)}")
    print(f"PASS: verified context invariance in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
