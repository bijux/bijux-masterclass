from __future__ import annotations

import copy
import unittest

from scripts.program_qualification.provenance import (
    REQUIRED_CONTEXTS,
    admit_saved_qualification,
)


class AcceptedProgramQualificationTests(unittest.TestCase):
    def evidence(self):
        identity = {
            "profile": "fast",
            "program": "deep-dive-snakemake",
            "sources": "inputs",
            "runtime": "python-and-packages",
            "dependencies_locked": True,
        }
        receipt = {
            "schema_version": 1,
            "worktree_clean": True,
            "result": "success",
            "execution": "executed",
            "identity": identity,
            "execution_tree": "tree",
            "run_id": 20,
            "run_attempt": 1,
            "job_name": "deep-dive-snakemake-fast",
        }
        run = {
            "id": 20,
            "run_attempt": 1,
            "head_sha": "head",
            "path": ".github/workflows/program-validation.yml",
            "name": "Program Validation",
            "repository": {"full_name": "bijux/bijux-masterclass"},
            "head_repository": {"full_name": "bijux/bijux-masterclass"},
            "status": "completed",
            "conclusion": "success",
            "event": "pull_request",
        }
        pr = {
            "state": "closed",
            "merged": True,
            "merge_commit_sha": "merge",
            "user": {"login": "bijux"},
            "base": {
                "sha": "base",
                "ref": "main",
                "repo": {"full_name": "bijux/bijux-masterclass"},
            },
            "head": {"sha": "head", "repo": {"full_name": "bijux/bijux-masterclass"}},
        }
        merge = {
            "sha": "merge",
            "parents": [{"sha": "base"}, {"sha": "head"}],
            "commit": {"tree": {"sha": "tree"}},
        }
        artifact = {"expired": False, "workflow_run": {"id": 20, "head_sha": "head"}}
        job = {
            "run_id": 20,
            "name": receipt["job_name"],
            "status": "completed",
            "conclusion": "success",
            "check_run_url": "https://api.github.com/check-runs/30",
        }
        check = {
            "id": 30,
            "name": job["name"],
            "app": {"id": 15368},
            "head_sha": "head",
            "status": "completed",
            "conclusion": "success",
        }
        checks = [
            dict(check, id=40 + i, name=context)
            for i, context in enumerate(sorted(REQUIRED_CONTEXTS))
        ]
        return {
            "receipt": receipt,
            "expected_identity": identity,
            "artifact": artifact,
            "run": run,
            "job": job,
            "check": check,
            "accepted_pr": pr,
            "merge": merge,
            "head_checks": checks,
            "accepted_ancestor": True,
        }

    def test_exact_successful_accepted_program_execution_authorizes_reuse(self):
        admit_saved_qualification(**self.evidence())

    def test_manual_full_qualification_has_distinct_accepted_execution_identity(self):
        proof = self.evidence()
        proof["run"].update(
            event="workflow_dispatch", head_sha="merge", actor={"login": "bijux"}
        )
        proof["artifact"]["workflow_run"]["head_sha"] = "merge"
        proof["check"]["head_sha"] = "merge"
        admit_saved_qualification(**proof)

    def test_wrong_foreign_failed_missing_and_stale_evidence_cannot_skip_tests(self):
        changes = [
            ("receipt", ("schema_version",), 2),
            ("receipt", ("worktree_clean",), False),
            ("receipt", ("result",), "failure"),
            ("receipt", ("execution",), "reused"),
            ("receipt", ("execution_tree",), "different"),
            ("receipt", ("run_id",), 21),
            ("receipt", ("run_attempt",), 2),
            ("expected_identity", ("dependencies_locked",), False),
            ("expected_identity", ("profile",), "full"),
            ("expected_identity", ("sources",), "new-inputs"),
            ("expected_identity", ("runtime",), "new-python-or-tool"),
            ("artifact", ("expired",), True),
            ("artifact", ("workflow_run", "id"), 21),
            ("artifact", ("workflow_run", "head_sha"), "foreign"),
            ("run", ("conclusion",), "failure"),
            ("run", ("status",), "in_progress"),
            ("run", ("event",), "push"),
            ("run", ("head_sha",), "foreign"),
            ("run", ("path",), ".github/workflows/unrelated.yml"),
            ("run", ("head_repository", "full_name"), "fork/masterclass"),
            ("accepted_pr", ("merged",), False),
            ("accepted_pr", ("user", "login"), "dependabot[bot]"),
            ("accepted_pr", ("head", "repo", "full_name"), "fork/masterclass"),
            ("accepted_pr", ("base", "ref"), "other"),
            ("accepted_pr", ("merge_commit_sha",), "unrelated"),
            ("job", ("conclusion",), "skipped"),
            ("job", ("name",), "other"),
            ("job", ("run_id",), 21),
            ("check", ("app", "id"), 9),
            ("check", ("head_sha",), "foreign"),
            ("check", ("conclusion",), "failure"),
        ]
        for root, path, value in changes:
            proof = copy.deepcopy(self.evidence())
            # Keep independently supplied expected identity separate from saved bytes.
            proof["expected_identity"] = copy.deepcopy(proof["expected_identity"])
            cursor = proof[root]
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = value
            with self.subTest(root=root, path=path), self.assertRaises(ValueError):
                admit_saved_qualification(**proof)
        for change in ["ancestry", "parents", "required", "latest"]:
            proof = self.evidence()
            if change == "ancestry":
                proof["accepted_ancestor"] = False
            if change == "parents":
                proof["merge"]["parents"] = [{"sha": "head"}]
            if change == "required":
                proof["head_checks"] = []
            if change == "latest":
                proof["head_checks"].append(
                    dict(proof["head_checks"][0], id=100, conclusion="failure")
                )
            with self.subTest(change=change), self.assertRaises(ValueError):
                admit_saved_qualification(**proof)


if __name__ == "__main__":
    unittest.main()
