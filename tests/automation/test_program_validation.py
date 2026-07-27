from __future__ import annotations

import unittest
from pathlib import Path

from scripts.program_validation import (
    PROGRAM_TARGETS,
    ROOT_CONTRACT,
    SERIES_SITE,
    select_validation_targets,
)


class ProgramValidationSelectionTests(unittest.TestCase):
    def names(self, paths: list[str], *, select_all: bool = False) -> list[str]:
        return [
            target["name"]
            for target in select_validation_targets(paths, select_all=select_all)
        ]

    def test_isolated_capstone_change_selects_only_its_program(self) -> None:
        names = self.names(
            [
                "programs/reproducible-research/deep-dive-snakemake/"
                "capstone/scripts/audit_scheduler_policy.py"
            ]
        )
        self.assertEqual(names, ["deep-dive-snakemake"])

    def test_course_book_change_adds_series_integration(self) -> None:
        names = self.names(
            [
                "programs/reproducible-research/deep-dive-snakemake/"
                "course-book/module-03-production-operations-policy-boundaries/index.md"
            ]
        )
        self.assertEqual(names, ["series-site", "deep-dive-snakemake"])

    def test_capstone_documentation_change_adds_series_integration(self) -> None:
        names = self.names(
            [
                "programs/reproducible-research/deep-dive-make/"
                "capstone/docs/proof-guide.md"
            ]
        )
        self.assertEqual(names, ["series-site", "deep-dive-make"])

    def test_root_make_change_selects_every_target(self) -> None:
        names = self.names(["makes/root.mk"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_TARGETS),
            ],
        )

    def test_dispatcher_change_uses_root_contract_not_every_program(self) -> None:
        names = self.names(["makes/program.mk"])
        self.assertEqual(names, [ROOT_CONTRACT.name])

    def test_dispatcher_change_retains_explicitly_affected_program(self) -> None:
        names = self.names(
            [
                "makes/program.mk",
                "programs/reproducible-research/deep-dive-snakemake/"
                "capstone/Makefile",
            ]
        )
        self.assertEqual(names, [ROOT_CONTRACT.name, "deep-dive-snakemake"])

    def test_shared_docs_make_change_selects_every_target(self) -> None:
        names = self.names(["makes/docs.mk"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_TARGETS),
            ],
        )

    def test_shared_mkdocs_change_selects_every_target(self) -> None:
        names = self.names(["mkdocs.shared.yml"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_TARGETS),
            ],
        )

    def test_selector_change_selects_every_target(self) -> None:
        names = self.names(["scripts/program_validation.py"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_TARGETS),
            ],
        )

    def test_family_index_selects_only_series_integration(self) -> None:
        names = self.names(["programs/python-programming/README.md"])
        self.assertEqual(names, ["series-site"])

    def test_shared_documentation_shell_selects_series_integration(self) -> None:
        names = self.names(
            [".bijux/shared/bijux-docs/tooling/templates/overrides/main.html"]
        )
        self.assertEqual(names, ["series-site"])

    def test_unrelated_governance_change_selects_no_heavy_target(self) -> None:
        names = self.names([".github/labeler.yml"])
        self.assertEqual(names, [])

    def test_manual_run_selects_every_target(self) -> None:
        names = self.names([], select_all=True)
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_TARGETS),
            ],
        )

    def test_path_normalization_deduplicates_selected_targets(self) -> None:
        names = self.names(
            [
                "./programs/python-programming/python-meta-programming/"
                "capstone/src/metacap/runtime.py",
                "programs/python-programming/python-meta-programming/"
                "course-book/module-01/index.md",
            ]
        )
        self.assertEqual(names, ["series-site", "python-meta-programming"])


class WorkflowEconomyTests(unittest.TestCase):
    repository_root = Path(__file__).resolve().parents[2]

    def workflow_text(self, name: str) -> str:
        return (
            self.repository_root / ".github" / "workflows" / name
        ).read_text(encoding="utf-8")

    def test_program_validation_does_not_repeat_after_merge(self) -> None:
        workflow = self.workflow_text("program-validation.yml")
        self.assertNotIn("\n  push:\n", workflow)
        self.assertIn("\n  pull_request:\n", workflow)
        self.assertIn("cancel-in-progress: true", workflow)

    def test_program_validation_uses_affected_target_matrix(self) -> None:
        workflow = self.workflow_text("program-validation.yml")
        self.assertIn("scripts/program_validation.py", workflow)
        self.assertIn("fromJSON(needs.select.outputs.matrix)", workflow)
        self.assertNotIn("matrix:\n        include:", workflow)

    def test_pages_only_runs_for_publication_inputs(self) -> None:
        workflow = self.workflow_text("pages.yml")
        self.assertIn('"programs/*/*/course-book/**"', workflow)
        self.assertIn('"programs/*/*/capstone/docs/**"', workflow)
        self.assertIn('".bijux/shared/bijux-docs/**"', workflow)
        self.assertNotIn('"programs/**"', workflow)

    def test_pages_does_not_install_dependencies_twice(self) -> None:
        workflow = self.workflow_text("pages.yml")
        self.assertNotIn("Install documentation dependencies", workflow)
        self.assertEqual(workflow.count("make series-docs-build"), 1)

    def test_repository_owned_workflows_pin_action_revisions(self) -> None:
        workflows = (
            self.workflow_text("program-validation.yml"),
            self.workflow_text("pages.yml"),
        )
        for workflow in workflows:
            self.assertNotIn("uses: actions/checkout@v", workflow)
            self.assertNotIn("uses: actions/setup-python@v", workflow)


if __name__ == "__main__":
    unittest.main()
