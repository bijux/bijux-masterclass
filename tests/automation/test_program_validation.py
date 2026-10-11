from __future__ import annotations

import unittest
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from docs.hooks.publish_site_assets import on_post_build
from scripts.program_validation import (
    PROGRAM_DOCUMENTATION_TARGETS,
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
                (
                    "programs/reproducible-research/deep-dive-snakemake/"
                    "capstone/scripts/audit_scheduler_policy.py"
                )
            ]
        )
        self.assertEqual(
            names, ["deep-dive-snakemake-documentation", "deep-dive-snakemake-fast"]
        )

    def test_catalogue_planning_domain_selects_only_series_integration(self) -> None:
        self.assertEqual(
            self.names(["scripts/catalogue/source_plan.py"]), ["series-site"]
        )

    def test_course_book_change_adds_series_integration(self) -> None:
        names = self.names(
            [
                (
                    "programs/reproducible-research/deep-dive-snakemake/"
                    "course-book/module-03-production-operations-policy-boundaries/index.md"
                )
            ]
        )
        self.assertEqual(names, ["series-site", "deep-dive-snakemake-documentation"])

    def test_capstone_documentation_change_adds_series_integration(self) -> None:
        names = self.names(
            [
                (
                    "programs/reproducible-research/deep-dive-make/"
                    "capstone/docs/proof-guide.md"
                )
            ]
        )
        self.assertEqual(names, ["series-site", "deep-dive-make-documentation"])

    def test_root_make_change_selects_every_target(self) -> None:
        names = self.names(["makes/root.mk"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
                *(target.name + "-fast" for target in PROGRAM_TARGETS),
            ],
        )

    def test_dispatcher_recipe_change_selects_native_and_documentation_obligations(
        self,
    ) -> None:
        names = self.names(["makes/program.mk"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
                *(target.name + "-fast" for target in PROGRAM_TARGETS),
            ],
        )

    def test_dispatcher_change_retains_explicitly_affected_program(self) -> None:
        names = self.names(
            [
                "makes/program.mk",
                (
                    "programs/reproducible-research/deep-dive-snakemake/"
                    "capstone/Makefile"
                ),
            ]
        )
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
                *(target.name + "-fast" for target in PROGRAM_TARGETS),
            ],
        )

    def test_shared_docs_make_change_selects_every_target(self) -> None:
        names = self.names(["makes/docs.mk"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
            ],
        )

    def test_shared_mkdocs_change_selects_every_target(self) -> None:
        names = self.names(["mkdocs.shared.yml"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
            ],
        )

    def test_selector_change_selects_every_target(self) -> None:
        names = self.names(["scripts/program_validation.py"])
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
                *(target.name + "-fast" for target in PROGRAM_TARGETS),
            ],
        )

    def test_family_index_selects_only_series_integration(self) -> None:
        names = self.names(["programs/python-programming/README.md"])
        self.assertEqual(names, ["series-site"])

    def test_shared_documentation_shell_selects_series_integration(self) -> None:
        names = self.names(
            [".bijux/shared/bijux-docs/tooling/templates/overrides/main.html"]
        )
        self.assertEqual(
            names,
            [
                ROOT_CONTRACT.name,
                SERIES_SITE.name,
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
            ],
        )

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
                *(target.name for target in PROGRAM_DOCUMENTATION_TARGETS),
                *(target.name + "-full" for target in PROGRAM_TARGETS),
            ],
        )

    def test_path_normalization_deduplicates_selected_targets(self) -> None:
        names = self.names(
            [
                (
                    "./programs/python-programming/python-meta-programming/"
                    "capstone/src/metacap/runtime.py"
                ),
                (
                    "programs/python-programming/python-meta-programming/"
                    "course-book/module-01/index.md"
                ),
            ]
        )
        self.assertEqual(
            names,
            [
                "series-site",
                "python-meta-programming-documentation",
                "python-meta-programming-fast",
            ],
        )


class WorkflowEconomyTests(unittest.TestCase):
    repository_root = Path(__file__).resolve().parents[2]

    def workflow_text(self, name: str) -> str:
        return (self.repository_root / ".github" / "workflows" / name).read_text(
            encoding="utf-8"
        )

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

    def test_documentation_publication_requires_manual_admission(self) -> None:
        workflow = self.workflow_text("deploy-docs.yml")
        self.assertIn('"workflow_dispatch":', workflow)
        for event in ("push", "pull_request", "workflow_call"):
            self.assertNotIn(f'  "{event}":', workflow)
        self.assertIn("publication_admission.py", workflow)
        self.assertFalse(
            (self.repository_root / ".github" / "workflows" / "pages.yml").exists()
        )

    def test_documentation_publication_builds_the_series_once(self) -> None:
        workflow = self.workflow_text("deploy-docs.yml")
        adapter = (self.repository_root / ".github" / "docs-deploy.env").read_text(
            encoding="utf-8"
        )
        self.assertIn("BIJUX_DOCS_BUILD_COMMAND='make series-docs-build'", adapter)
        self.assertNotIn("Install documentation dependencies", workflow)
        self.assertEqual(adapter.count("make series-docs-build"), 1)

    def test_functional_confirmation_executes_pytest_once(self) -> None:
        capstone = (
            self.repository_root
            / "programs"
            / "python-programming"
            / "python-functional-programming"
            / "capstone"
        )
        result = run(
            ["make", "--dry-run", "confirm"],
            cwd=capstone,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout.count("/bin/pytest -q"), 1)

    def test_repository_owned_workflows_pin_action_revisions(self) -> None:
        workflows = (
            self.workflow_text("program-validation.yml"),
            self.workflow_text("deploy-docs.yml"),
        )
        for workflow in workflows:
            self.assertNotIn("uses: actions/checkout@v", workflow)
            self.assertNotIn("uses: actions/setup-python@v", workflow)

    def test_standalone_program_sites_publish_shared_assets(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            site_dir = temporary_root / "site"
            config = SimpleNamespace(
                docs_dir=str(temporary_root / "staged-course-book"),
                site_dir=str(site_dir),
            )

            on_post_build(config)

            self.assertTrue(
                (site_dir / "assets" / "javascripts" / "mermaid-init.js").is_file()
            )
            self.assertTrue(
                (
                    site_dir
                    / "assets"
                    / "javascripts"
                    / "vendor"
                    / "mermaid-11.6.0.min.js"
                ).is_file()
            )
            self.assertTrue((site_dir / "assets" / "styles" / "extra.css").is_file())
            self.assertTrue((site_dir / "favicon.ico").is_file())

    def test_program_configs_use_site_local_shared_asset_urls(self) -> None:
        program_configs = self.repository_root.glob("programs/*/*/mkdocs.yml")

        for config_path in program_configs:
            with self.subTest(config_path=config_path):
                config = config_path.read_text(encoding="utf-8")
                self.assertNotIn("../../../docs/assets", config)


if __name__ == "__main__":
    unittest.main()
