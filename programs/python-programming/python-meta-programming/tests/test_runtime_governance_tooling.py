from __future__ import annotations

import importlib
import sys
import unittest

from labs.runtime_governance.tooling import (
    installed_virtual_module,
    rewrite_constant,
    tooling_evidence,
)


class ToolingGovernanceTests(unittest.TestCase):
    module_name = "_bijux_runtime_governance_test_module"

    def tearDown(self) -> None:
        sys.modules.pop(self.module_name, None)

    def test_virtual_module_exists_only_while_hook_is_installed(self) -> None:
        with installed_virtual_module(
            self.module_name,
            {"status": "virtual"},
        ) as finder:
            module = importlib.import_module(self.module_name)
            self.assertEqual(module.status, "virtual")  # type: ignore[attr-defined]
            self.assertIn(finder, sys.meta_path)

        self.assertNotIn(finder, sys.meta_path)
        self.assertNotIn(self.module_name, sys.modules)
        with self.assertRaises(ModuleNotFoundError):
            importlib.import_module(self.module_name)

    def test_finder_ignores_every_other_module_name(self) -> None:
        with installed_virtual_module(self.module_name, {}) as finder:
            self.assertIsNone(finder.find_spec("json"))
            self.assertEqual(finder.events, [])

    def test_existing_module_name_is_refused(self) -> None:
        sys.modules[self.module_name] = importlib.import_module("json")

        with self.assertRaisesRegex(RuntimeError, "module already loaded"):
            with installed_virtual_module(self.module_name, {}):
                pass

    def test_ast_transform_reports_exact_replacement_count(self) -> None:
        result, replacements = rewrite_constant(
            "result = 'draft' + ':' + 'draft'",
            "draft",
            "approved",
        )

        self.assertEqual(result, "approved:approved")
        self.assertEqual(replacements, 2)

    def test_ast_transform_preserves_unmatched_constants(self) -> None:
        result, replacements = rewrite_constant(
            "result = 'unchanged'",
            "draft",
            "approved",
        )

        self.assertEqual(result, "unchanged")
        self.assertEqual(replacements, 0)

    def test_evidence_requires_cleanup_and_no_hook_mode(self) -> None:
        evidence = tooling_evidence()
        hook = evidence["import_hook"]

        self.assertEqual(  # type: ignore[index]
            hook["events"],
            [
                "find:_bijux_runtime_governance_virtual",
                "create:_bijux_runtime_governance_virtual",
                "exec:_bijux_runtime_governance_virtual",
            ],
        )
        self.assertFalse(hook["hook_present_after_scope"])  # type: ignore[index]
        self.assertFalse(hook["module_cached_after_scope"])  # type: ignore[index]
        self.assertTrue(evidence["boundaries"]["no_hook_mode_required"])  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
