"""Admit saved results only from an exact successful accepted execution."""

from __future__ import annotations

from typing import Any

REPOSITORY = "bijux/bijux-masterclass"
WORKFLOW = ".github/workflows/program-validation.yml"
REQUIRED_CONTEXTS = {
    "policy / github",
    "policy / pr approval",
    "std / standard",
    "std / report",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def admit_saved_qualification(
    receipt: dict[str, Any],
    *,
    expected_identity: dict[str, Any],
    artifact: dict[str, Any],
    run: dict[str, Any],
    job: dict[str, Any],
    check: dict[str, Any],
    accepted_pr: dict[str, Any],
    merge: dict[str, Any],
    head_checks: list[dict[str, Any]],
    accepted_ancestor: bool,
) -> None:
    require(receipt.get("schema_version") == 1, "unsupported qualification schema")
    require(
        receipt.get("result") == "success" and receipt.get("execution") == "executed",
        "a reusable receipt must originate in actual successful execution",
    )
    require(
        receipt.get("worktree_clean") is True,
        "dirty local context cannot authorize reuse",
    )
    require(
        receipt.get("identity") == expected_identity, "qualification inputs changed"
    )
    require(
        expected_identity.get("dependencies_locked") is True,
        "floating dependencies must execute",
    )
    require(accepted_ancestor, "qualification source is not accepted main ancestry")
    require(
        accepted_pr.get("merged") is True and accepted_pr.get("state") == "closed",
        "qualification PR was not accepted",
    )
    require(
        accepted_pr.get("base", {}).get("repo", {}).get("full_name") == REPOSITORY
        and accepted_pr.get("base", {}).get("ref") == "main",
        "foreign accepted base",
    )
    require(
        accepted_pr.get("head", {}).get("repo", {}).get("full_name") == REPOSITORY,
        "fork artifacts cannot authorize reuse",
    )
    require(
        accepted_pr.get("user", {}).get("login") == "bijux",
        "untrusted original PR author",
    )
    parents = [parent.get("sha") for parent in merge.get("parents", [])]
    head = accepted_pr.get("head", {}).get("sha")
    require(
        len(parents) == 2 and parents == [accepted_pr.get("base", {}).get("sha"), head],
        "qualification is not an exact normal PR merge",
    )
    require(
        merge.get("sha") == accepted_pr.get("merge_commit_sha"),
        "different accepted merge",
    )
    require(
        merge.get("commit", {}).get("tree", {}).get("sha")
        == receipt.get("execution_tree"),
        "accepted tree differs from executed tree",
    )
    require(
        run.get("repository", {}).get("full_name") == REPOSITORY
        and run.get("head_repository", {}).get("full_name") == REPOSITORY,
        "foreign qualification workflow",
    )
    require(
        run.get("path") == WORKFLOW and run.get("name") == "Program Validation",
        "different qualification workflow",
    )
    require(
        run.get("status") == "completed" and run.get("conclusion") == "success",
        "qualification workflow did not complete successfully",
    )
    require(
        run.get("event") in {"pull_request", "workflow_dispatch"},
        "unsupported qualification event",
    )
    if run["event"] == "pull_request":
        require(
            run.get("head_sha") == head, "qualification ran against a different PR head"
        )
    else:
        require(
            run.get("head_sha") == merge.get("sha")
            and run.get("actor", {}).get("login") == "bijux",
            "untrusted manual qualification",
        )
    require(
        run.get("id")
        == receipt.get("run_id")
        == artifact.get("workflow_run", {}).get("id"),
        "artifact run does not match the executed receipt",
    )
    require(
        run.get("run_attempt") == receipt.get("run_attempt"),
        "different qualification attempt",
    )
    require(
        artifact.get("expired") is False
        and artifact.get("workflow_run", {}).get("head_sha") == run.get("head_sha"),
        "expired or foreign-head artifact",
    )
    require(
        job.get("run_id") == run.get("id")
        and job.get("name") == receipt.get("job_name")
        and job.get("status") == "completed"
        and job.get("conclusion") == "success",
        "qualification job did not execute successfully",
    )
    require(
        check.get("id") == int(job.get("check_run_url", "").rsplit("/", 1)[-1])
        and check.get("app", {}).get("id") == 15368
        and check.get("head_sha") == run.get("head_sha")
        and check.get("status") == "completed"
        and check.get("conclusion") == "success"
        and check.get("name") == job.get("name"),
        "foreign or failed execution context",
    )
    latest: dict[str, dict[str, Any]] = {}
    for row in head_checks:
        if row.get("name") not in latest or row["id"] > latest[row["name"]]["id"]:
            latest[row["name"]] = row
    for context in REQUIRED_CONTEXTS:
        row = latest.get(context, {})
        require(
            row.get("app", {}).get("id") == 15368
            and row.get("head_sha") == head
            and row.get("status") == "completed"
            and row.get("conclusion") == "success",
            f"accepted-head context was not verified: {context}",
        )
