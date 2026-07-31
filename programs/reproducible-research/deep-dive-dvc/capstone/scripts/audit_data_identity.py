#!/usr/bin/env python3
"""Audit DVC content identity and recovery boundaries in isolated repositories."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path,
    evidence_dir: Path,
    name: str,
    env: dict[str, str],
    expect_success: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        capture_output=True,
    )
    (evidence_dir / f"{name}.stdout.txt").write_text(
        completed.stdout, encoding="utf-8"
    )
    (evidence_dir / f"{name}.stderr.txt").write_text(
        completed.stderr, encoding="utf-8"
    )
    if expect_success and completed.returncode != 0:
        raise RuntimeError(
            f"{name} returned {completed.returncode}; inspect {evidence_dir}"
        )
    return completed


def finding(
    name: str,
    decision: str,
    checks: dict[str, bool],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "finding": name,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "decision": decision,
        "checks": checks,
        "evidence": evidence,
    }


def pointer(path: Path) -> dict[str, Any]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    return document["outs"][0]


def cache_object(repo: Path, md5: str) -> Path:
    return repo / ".dvc" / "cache" / "files" / "md5" / md5[:2] / md5[2:]


def prepare_case(
    name: str,
    *,
    specimen: Path,
    workspace: Path,
    evidence_dir: Path,
    dvc: list[str],
    env: dict[str, str],
) -> tuple[Path, Path, dict[str, Any]]:
    case = workspace / name
    shutil.copytree(specimen, case)
    tracked = case / "data" / "observations.csv"
    tracked.parent.mkdir()
    shutil.copy2(case / "source" / "observations.csv", tracked)
    run(
        [*dvc, "init", "--no-scm", "-q"],
        cwd=case,
        evidence_dir=evidence_dir,
        name=f"{name}-init",
        env=env,
    )
    run(
        [*dvc, "add", "data/observations.csv"],
        cwd=case,
        evidence_dir=evidence_dir,
        name=f"{name}-add",
        env=env,
    )
    return case, tracked, pointer(case / "data" / "observations.csv.dvc")


def write_summary(path: Path, findings: list[dict[str, Any]]) -> None:
    rows = ["finding\tresult\tdecision"]
    rows.extend(
        f"{item['finding']}\t{item['result']}\t{item['decision']}"
        for item in findings
    )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    args = parser.parse_args()

    specimen = args.specimen.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    python = args.python.absolute()
    dvc = [str(python), "-m", "dvc"]
    env = os.environ.copy()
    env["PATH"] = f"{python.parent}{os.pathsep}{env.get('PATH', '')}"

    shutil.rmtree(output.parent, ignore_errors=True)
    output.parent.mkdir(parents=True)
    workspace.mkdir(parents=True)
    evidence_dir = output.parent / "evidence"
    evidence_dir.mkdir()

    pointer_case, tracked, original_pointer = prepare_case(
        "pointer-cache",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    original_cache = cache_object(pointer_case, original_pointer["md5"])
    source_digest = sha256(pointer_case / "source" / "observations.csv")

    same_case, same_tracked, same_pointer = prepare_case(
        "same-content",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    relocated = same_case / "archive" / "renamed.csv"
    relocated.parent.mkdir()
    shutil.copy2(same_tracked, relocated)
    run(
        [*dvc, "add", "archive/renamed.csv"],
        cwd=same_case,
        evidence_dir=evidence_dir,
        name="same-content-add-relocated",
        env=env,
    )
    relocated_pointer = pointer(same_case / "archive" / "renamed.csv.dvc")

    changed_case, changed_tracked, changed_pointer_before = prepare_case(
        "changed-content",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    with changed_tracked.open("a", encoding="utf-8") as handle:
        handle.write("delta,13\n")
    run(
        [*dvc, "add", "data/observations.csv"],
        cwd=changed_case,
        evidence_dir=evidence_dir,
        name="changed-content-add",
        env=env,
    )
    changed_pointer_after = pointer(changed_case / "data" / "observations.csv.dvc")

    cache_case, cache_tracked, cache_pointer = prepare_case(
        "cache-recovery",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    cache_tracked.unlink()
    run(
        [*dvc, "checkout"],
        cwd=cache_case,
        evidence_dir=evidence_dir,
        name="cache-recovery-checkout",
        env=env,
    )

    remote_case, remote_tracked, remote_pointer = prepare_case(
        "remote-recovery",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    run(
        [*dvc, "remote", "add", "-d", "identity-store", ".identity-remote"],
        cwd=remote_case,
        evidence_dir=evidence_dir,
        name="remote-recovery-configure",
        env=env,
    )
    run(
        [*dvc, "push"],
        cwd=remote_case,
        evidence_dir=evidence_dir,
        name="remote-recovery-push",
        env=env,
    )
    remote_tracked.unlink()
    shutil.rmtree(remote_case / ".dvc" / "cache")
    run(
        [*dvc, "pull"],
        cwd=remote_case,
        evidence_dir=evidence_dir,
        name="remote-recovery-pull",
        env=env,
    )
    run(
        [*dvc, "checkout"],
        cwd=remote_case,
        evidence_dir=evidence_dir,
        name="remote-recovery-checkout",
        env=env,
    )

    missing_case, missing_tracked, missing_pointer = prepare_case(
        "pointer-only",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    missing_tracked.unlink()
    shutil.rmtree(missing_case / ".dvc" / "cache")
    missing_checkout = run(
        [*dvc, "checkout"],
        cwd=missing_case,
        evidence_dir=evidence_dir,
        name="pointer-only-checkout",
        env=env,
        expect_success=False,
    )

    findings = [
        finding(
            "POINTER_NAMES_CACHED_CONTENT",
            "ACCEPT",
            {
                "pointer_has_content_id": bool(original_pointer["md5"]),
                "pointer_size_matches_workspace": original_pointer["size"]
                == tracked.stat().st_size,
                "cache_object_exists": original_cache.is_file(),
                "cache_bytes_match_workspace": sha256(original_cache)
                == sha256(tracked),
            },
            {
                "pointer": original_pointer,
                "cache_object": original_cache.relative_to(pointer_case).as_posix(),
                "sha256": sha256(tracked),
            },
        ),
        finding(
            "SAME_BYTES_SHARE_IDENTITY",
            "ACCEPT",
            {
                "paths_differ": same_tracked != relocated,
                "workspace_bytes_match": sha256(same_tracked) == sha256(relocated),
                "pointer_ids_match": same_pointer["md5"]
                == relocated_pointer["md5"],
            },
            {
                "original_path": same_tracked.relative_to(same_case).as_posix(),
                "relocated_path": relocated.relative_to(same_case).as_posix(),
                "content_id": same_pointer["md5"],
            },
        ),
        finding(
            "CHANGED_BYTES_CHANGE_IDENTITY",
            "ACCEPT",
            {
                "workspace_path_is_stable": changed_pointer_before["path"]
                == changed_pointer_after["path"],
                "pointer_id_changes": changed_pointer_before["md5"]
                != changed_pointer_after["md5"],
                "new_cache_object_exists": cache_object(
                    changed_case, changed_pointer_after["md5"]
                ).is_file(),
            },
            {
                "before": changed_pointer_before["md5"],
                "after": changed_pointer_after["md5"],
                "path": changed_pointer_after["path"],
            },
        ),
        finding(
            "CACHE_RESTORES_WORKSPACE",
            "ACCEPT",
            {
                "workspace_is_restored": cache_tracked.is_file(),
                "restored_bytes_match_source": sha256(cache_tracked) == source_digest,
                "pointer_identity_is_unchanged": pointer(
                    cache_case / "data" / "observations.csv.dvc"
                )["md5"]
                == cache_pointer["md5"],
            },
            {
                "content_id": cache_pointer["md5"],
                "restored_sha256": sha256(cache_tracked),
            },
        ),
        finding(
            "REMOTE_RESTORES_AFTER_CACHE_LOSS",
            "ACCEPT",
            {
                "workspace_is_restored": remote_tracked.is_file(),
                "restored_bytes_match_source": sha256(remote_tracked) == source_digest,
                "cache_is_repopulated": cache_object(
                    remote_case, remote_pointer["md5"]
                ).is_file(),
            },
            {
                "content_id": remote_pointer["md5"],
                "restored_sha256": sha256(remote_tracked),
            },
        ),
        finding(
            "REMOTE_RECOVERY_PRESERVES_IDENTITY",
            "ACCEPT",
            {
                "pointer_id_matches_baseline": remote_pointer["md5"]
                == original_pointer["md5"],
                "restored_sha256_matches_baseline": sha256(remote_tracked)
                == sha256(tracked),
            },
            {
                "baseline_content_id": original_pointer["md5"],
                "recovered_content_id": remote_pointer["md5"],
            },
        ),
        finding(
            "POINTER_ONLY_IS_NOT_RECOVERABLE",
            "REJECT",
            {
                "pointer_still_names_content": bool(missing_pointer["md5"]),
                "checkout_fails": missing_checkout.returncode != 0,
                "workspace_remains_absent": not missing_tracked.exists(),
                "cache_object_remains_absent": not cache_object(
                    missing_case, missing_pointer["md5"]
                ).exists(),
            },
            {
                "content_id": missing_pointer["md5"],
                "checkout_returncode": missing_checkout.returncode,
            },
        ),
    ]

    report = {
        "specimen": specimen.as_posix(),
        "workspace": workspace.as_posix(),
        "findings": findings,
    }
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_summary(output.parent / "summary.tsv", findings)

    failed = [item["finding"] for item in findings if item["result"] != "PASS"]
    if failed:
        print(f"FAIL: data identity audit failed: {', '.join(failed)}")
        return 1
    print(f"PASS: audited data identity boundaries in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
