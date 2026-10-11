"""Read bounded GitHub evidence; absent or untrusted artifacts never skip work."""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import time
import zipfile
from pathlib import Path
from typing import Any

from .provenance import REPOSITORY, admit_saved_qualification


def api(endpoint: str, timeout: float = 30) -> Any:
    return json.loads(subprocess.check_output(["gh", "api", endpoint], timeout=timeout))


def read_receipt(artifact: dict[str, Any], timeout: float = 30) -> dict[str, Any]:
    if artifact.get("expired") or not 0 < artifact.get("size_in_bytes", 0) <= 2_000_000:
        raise ValueError(
            "artifact is unavailable or exceeds the qualification size limit"
        )
    archive = subprocess.check_output(
        ["gh", "api", f"repos/{REPOSITORY}/actions/artifacts/{artifact['id']}/zip"],
        timeout=timeout,
    )
    if artifact.get("digest") != "sha256:" + hashlib.sha256(archive).hexdigest():
        raise ValueError("qualification archive failed its GitHub digest")
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        entries = bundle.infolist()
        if (
            len(entries) != 1
            or entries[0].filename != "qualification.json"
            or entries[0].file_size > 1_000_000
        ):
            raise ValueError(
                "qualification artifact must contain exactly its bounded JSON receipt"
            )
        value = json.loads(bundle.read(entries[0]))
    if not isinstance(value, dict):
        raise TypeError("qualification receipt is not an object")
    return value


def find_saved_qualification(
    root: Path, identity: dict[str, Any], artifact_name: str
) -> dict[str, Any] | None:
    if identity.get("dependencies_locked") is not True:
        return None
    deadline = time.monotonic() + 12

    def remaining() -> float:
        budget = deadline - time.monotonic()
        if budget <= 0:
            raise ValueError("qualification lookup budget exhausted; execute instead")
        return budget

    def query(endpoint: str) -> Any:
        return api(endpoint, remaining())

    try:
        candidates = query(
            f"repos/{REPOSITORY}/actions/artifacts?name={artifact_name}&per_page=20"
        )["artifacts"]
    except (ValueError, KeyError, TypeError, subprocess.SubprocessError, OSError):
        return None
    for artifact in candidates[:20]:
        try:
            if artifact.get("name") != artifact_name:
                continue
            receipt = read_receipt(artifact, remaining())
            if receipt.get("identity") != identity:
                continue
            run = query(f"repos/{REPOSITORY}/actions/runs/{receipt['run_id']}")
            jobs = query(
                f"repos/{REPOSITORY}/actions/runs/{run['id']}/attempts/{run['run_attempt']}/jobs?per_page=100"
            )["jobs"]
            matches = [job for job in jobs if job["name"] == receipt.get("job_name")]
            if len(matches) != 1:
                continue
            job = matches[0]
            check = query(job["check_run_url"])
            related = query(
                f"repos/{REPOSITORY}/commits/{run['head_sha']}/pulls?per_page=100"
            )
            for related_pr in related:
                pr = query(f"repos/{REPOSITORY}/pulls/{related_pr['number']}")
                if not pr.get("merged") or not pr.get("merge_commit_sha"):
                    continue
                merge = query(f"repos/{REPOSITORY}/commits/{pr['merge_commit_sha']}")
                ancestry = (
                    subprocess.run(
                        [
                            "git",
                            "merge-base",
                            "--is-ancestor",
                            merge["sha"],
                            "origin/main",
                        ],
                        cwd=root,
                        capture_output=True,
                        check=False,
                    ).returncode
                    == 0
                )
                checks = query(
                    f"repos/{REPOSITORY}/commits/{pr['head']['sha']}/check-runs?per_page=100&filter=all"
                )
                if checks["total_count"] > 100:
                    continue
                admit_saved_qualification(
                    receipt,
                    expected_identity=identity,
                    artifact=artifact,
                    run=run,
                    job=job,
                    check=check,
                    accepted_pr=pr,
                    merge=merge,
                    head_checks=checks["check_runs"],
                    accepted_ancestor=ancestry,
                )
                return {
                    "artifact_id": artifact["id"],
                    "artifact_digest": artifact["digest"],
                    "run_id": run["id"],
                    "accepted_merge": merge["sha"],
                    "receipt": receipt,
                }
        except (
            ValueError,
            KeyError,
            TypeError,
            IndexError,
            subprocess.SubprocessError,
            OSError,
            zipfile.BadZipFile,
        ):
            continue
    return None
