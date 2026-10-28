from __future__ import annotations


def reconcile(
    *,
    control_artifact_refs: set[str],
    artifact_ids: set[str],
    completed_runs: set[str],
    notification_run_ids: set[str],
) -> list[str]:
    findings: list[str] = []
    for artifact_id in sorted(artifact_ids - control_artifact_refs):
        findings.append(f"orphan-artifact:{artifact_id}")
    for artifact_id in sorted(control_artifact_refs - artifact_ids):
        findings.append(f"missing-artifact:{artifact_id}")
    for run_id in sorted(completed_runs - notification_run_ids):
        findings.append(f"missing-notification:{run_id}")
    return findings
