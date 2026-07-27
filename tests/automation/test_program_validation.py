from __future__ import annotations

import unittest

from scripts.program_validation import (
    PROGRAM_TARGETS,
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

    def test_shared_make_change_selects_every_target(self) -> None:
        names = self.names(["makes/program.mk"])
        self.assertEqual(
            names,
            [SERIES_SITE.name, *(target.name for target in PROGRAM_TARGETS)],
        )

    def test_shared_mkdocs_change_selects_every_target(self) -> None:
        names = self.names(["mkdocs.shared.yml"])
        self.assertEqual(
            names,
            [SERIES_SITE.name, *(target.name for target in PROGRAM_TARGETS)],
        )

    def test_selector_change_selects_every_target(self) -> None:
        names = self.names(["scripts/program_validation.py"])
        self.assertEqual(
            names,
            [SERIES_SITE.name, *(target.name for target in PROGRAM_TARGETS)],
        )

    def test_family_index_selects_only_series_integration(self) -> None:
        names = self.names(["programs/python-programming/README.md"])
        self.assertEqual(names, ["series-site"])

    def test_unrelated_governance_change_selects_no_heavy_target(self) -> None:
        names = self.names([".github/labeler.yml"])
        self.assertEqual(names, [])

    def test_manual_run_selects_every_target(self) -> None:
        names = self.names([], select_all=True)
        self.assertEqual(
            names,
            [SERIES_SITE.name, *(target.name for target in PROGRAM_TARGETS)],
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


if __name__ == "__main__":
    unittest.main()
