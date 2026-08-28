from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.snippets import parse_snippets, verify_snippets

ARTIFACTS = ROOT / "artifacts"


def annotation(data: str, code: str, language: str = "python") -> str:
    return f"<!-- bijux-verify: {data} -->\n```{language}\n{code}\n```\n"


class SnippetParsingTests(unittest.TestCase):
    def test_executable_annotation_parses(self) -> None:
        text = annotation(
            '{"id":"sum-values","mode":"run","language":"python",'
            '"toolchain":"python3","expect":{"exit_code":0,"stdout":"6\\n"}}',
            "print(sum([1, 2, 3]))",
        )

        snippets, result = parse_snippets(text)

        self.assertEqual((), result.issues)
        self.assertEqual("sum-values", snippets[0].identifier)
        self.assertEqual("6\n", snippets[0].expect["stdout"])

    def test_unannotated_fence_fails(self) -> None:
        _, result = parse_snippets("```python\nprint('unsafe by omission')\n```\n")
        self.assertTrue(any("lacks an immediate" in issue for issue in result.issues))

    def test_schematic_requires_reason(self) -> None:
        text = annotation(
            '{"id":"protocol-shape","mode":"schematic","language":"python",'
            '"toolchain":"none","reason":""}',
            "send(message)",
        )
        _, result = parse_snippets(text)
        self.assertTrue(any("require a reason" in issue for issue in result.issues))

    def test_duplicate_ids_fail(self) -> None:
        item = annotation(
            '{"id":"duplicate","mode":"data","language":"json",'
            '"toolchain":"none","reason":"example payload"}',
            "{}",
            "json",
        )
        _, result = parse_snippets(item + "\n" + item)
        self.assertTrue(any("duplicate snippet ids" in issue for issue in result.issues))


class SnippetExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        ARTIFACTS.mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=ARTIFACTS)
        self.root = Path(self.directory.name)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_python_output_is_verified_and_reported(self) -> None:
        text = annotation(
            '{"id":"sum-values","mode":"run","language":"python",'
            '"toolchain":"python3","expect":{"exit_code":0,"stdout":"6\\n",'
            '"stderr":""}}',
            "print(sum([1, 2, 3]))",
        )

        result, report, path = verify_snippets(self.root, "PLS-001", text)

        self.assertEqual((), result.issues)
        self.assertEqual("passed", report.entries[0]["status"])
        self.assertTrue(path.is_file())
        self.assertEqual(1, report.counts["passed"])

    def test_output_mismatch_fails(self) -> None:
        text = annotation(
            '{"id":"wrong-output","mode":"run","language":"python",'
            '"toolchain":"python3","expect":{"exit_code":0,"stdout":"7\\n"}}',
            "print(6)",
        )
        result, report, _ = verify_snippets(self.root, "PLS-001", text)
        self.assertTrue(any("stdout differs" in issue for issue in result.issues))
        self.assertEqual("failed", report.entries[0]["status"])

    def test_python_compile_mode_is_verified(self) -> None:
        text = annotation(
            '{"id":"typed-binding","mode":"compile","language":"python",'
            '"toolchain":"python3","expect":{"exit_code":0,"stderr":""}}',
            "value: int = 6",
        )
        result, report, _ = verify_snippets(self.root, "PLS-001", text)
        self.assertEqual((), result.issues)
        self.assertEqual("passed", report.entries[0]["status"])

    def test_expected_failure_can_match_stderr(self) -> None:
        text = annotation(
            '{"id":"expected-error","mode":"run","language":"python",'
            '"toolchain":"python3","expect":{"exit_code":1,'
            '"stderr_contains":"ValueError: boom"}}',
            "raise ValueError('boom')",
        )
        result, report, _ = verify_snippets(self.root, "PLS-001", text)
        self.assertEqual((), result.issues)
        self.assertEqual("passed", report.entries[0]["status"])

    def test_external_state_call_is_rejected(self) -> None:
        text = annotation(
            '{"id":"write-file","mode":"run","language":"python",'
            '"toolchain":"python3","expect":{"exit_code":0}}',
            "open('outside.txt', 'w').write('no')",
        )
        result, report, _ = verify_snippets(self.root, "PLS-001", text)
        self.assertTrue(any("open" in issue for issue in result.issues))
        self.assertEqual("failed", report.entries[0]["status"])

    def test_unsupported_execution_route_is_unavailable(self) -> None:
        text = annotation(
            '{"id":"native-example","mode":"compile","language":"c",'
            '"toolchain":"cc","expect":{"exit_code":0}}',
            "int main(void) { return 0; }",
            "c",
        )
        result, report, _ = verify_snippets(self.root, "CA-001", text)
        self.assertTrue(any("unsupported execution route" in issue for issue in result.issues))
        self.assertEqual("unavailable", report.entries[0]["status"])

    def test_parse_failures_are_in_the_report(self) -> None:
        result, report, path = verify_snippets(
            self.root,
            "PLS-001",
            "```python\nprint('unannotated')\n```\n",
        )
        self.assertFalse(result.ok)
        self.assertEqual("failed", report.as_dict()["validation_status"])
        self.assertTrue(report.issues)
        self.assertTrue(path.is_file())

    def test_parse_failure_prevents_other_snippets_from_running(self) -> None:
        valid = annotation(
            '{"id":"would-run","mode":"run","language":"python",'
            '"toolchain":"python3","expect":{"exit_code":0}}',
            "print('not executed')",
        )
        result, report, _ = verify_snippets(
            self.root,
            "PLS-001",
            valid + "\n```python\nprint('unannotated')\n```\n",
        )
        self.assertFalse(result.ok)
        self.assertEqual((), report.entries)
        self.assertFalse(
            (self.root / "artifacts" / "snippets" / "PLS-001" / "would-run.py").exists()
        )

    def test_schematic_is_recorded_as_skipped(self) -> None:
        text = annotation(
            '{"id":"scheduler-model","mode":"schematic","language":"python",'
            '"toolchain":"none","reason":"requires a kernel scheduler"}',
            "schedule(task)",
        )
        result, report, _ = verify_snippets(self.root, "OS-001", text)
        self.assertEqual((), result.issues)
        self.assertEqual("skipped", report.entries[0]["status"])


if __name__ == "__main__":
    unittest.main()
