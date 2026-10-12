from __future__ import annotations

import os
import json
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(os.environ.get("BIJUX_TEST_DOCS_AUTHORITY_ROOT", Path(__file__).resolve().parents[2]))
SOURCE_SCRIPT = Path(os.environ.get("BIJUX_TEST_DOCS_SOURCE_SCRIPT", ROOT / "scripts/verify_docs_source.sh"))


class DocumentationAuthorityTests(unittest.TestCase):
    def test_make_children_isolate_program_source_context(self) -> None:
        artifact_root = ROOT / "artifacts" / "tests" / "documentation-authority"
        artifact_root.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=artifact_root) as temporary:
            fixture = Path(temporary)
            script = fixture / "scripts" / "verify_docs_source.sh"
            script.parent.mkdir()
            script.write_text(
                "#!/usr/bin/env bash\n"
                "set -euo pipefail\n"
                "test -z \"${BIJUX_STD_ROOT+x}\"\n"
                "test -z \"${BIJUX_STD_REF+x}\"\n"
                "printf '%s\\n' \"${1:-check}\"\n"
            )
            makefile = fixture / "Makefile"
            makefile.write_text(
                "SHELL := /bin/sh\n.SHELLFLAGS := -eu -c\n"
                f"include {ROOT / 'makes/bijux-docs.mk'}\n"
                f"include {ROOT / 'makes/bijux-std.mk'}\n"
                "series-docs-install:\n\t@:\n"
            )
            environment = dict(
                os.environ,
                BIJUX_STD_ROOT=str(fixture / "program-source"),
                BIJUX_STD_REF="1ad55aafdb44e2d47890632653e7d9c312cc7968",
            )
            command = [
                "make", "--no-print-directory",
                f"BIJUX_DOCS_SOURCE_SCRIPT={script}",
                f"BIJUX_DOCS_LOG_DIR={fixture / 'artifacts/logs'}",
                "VENV_PY=/usr/bin/true",
            ]
            for target, mode in (
                ("bijux-docs-sync", "sync"),
                ("bijux-docs-check", "check"),
                ("docs-source-check", "check"),
            ):
                with self.subTest(target=target):
                    result = subprocess.run(
                        [*command, target], cwd=fixture, env=environment,
                        text=True, capture_output=True, check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout.strip(), mode)
            result = subprocess.run(
                [*command, "VENV_PY=/usr/bin/false", "bijux-docs-check"],
                cwd=fixture, env=environment,
                text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0, "tee hid contract refusal")
            self.assertNotIn("check", result.stdout)
            script.write_text("#!/usr/bin/env bash\nexit 17\n")
            result = subprocess.run(
                [*command, "bijux-docs-check"], cwd=fixture, env=environment,
                text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0, "tee hid source refusal")

    def test_direct_wrong_documentation_pin_is_refused(self) -> None:
        result = subprocess.run(
            ["bash", str(SOURCE_SCRIPT)], cwd=ROOT,
            env=dict(os.environ, BIJUX_STD_REF="0" * 40),
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("override differs from the declared source pin", result.stderr)

    def test_unknown_source_mode_is_refused(self) -> None:
        result = subprocess.run(
            ["bash", str(SOURCE_SCRIPT), "foreign-mode"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mode must be check or sync", result.stderr)


class WorkflowPolicyAuthorityTests(unittest.TestCase):
    def fixture(self, mutate):
        artifacts = ROOT / "artifacts/tests/workflow-policy-authority"
        artifacts.mkdir(parents=True, exist_ok=True)
        sandbox = TemporaryDirectory(dir=artifacts)
        self.addCleanup(sandbox.cleanup)
        target = Path(sandbox.name)
        subprocess.run(["git", "init", "-q", str(target)], check=True)
        pins = target / ".github/standards"
        pins.mkdir(parents=True)
        (pins / "bijux-docs.sha").write_text("a" * 40 + "\n")
        authority = pins / "dependency-notification-source.json"
        record = dict(schema=1, repository="bijux-masterclass",
                      baseline_sha="1ad55aafdb44e2d47890632653e7d9c312cc7968",
                      execution_policy_sha="b" * 40)
        authority.write_text(json.dumps(record) + "\n")
        subprocess.run(["git", "-C", str(target), "add", ".github"], check=True)
        mutate(target, authority, record)
        environment = dict(os.environ)
        environment.pop("BIJUX_STD_REF", None)
        environment.pop("BIJUX_STD_ROOT", None)
        result = subprocess.run(["bash", str(SOURCE_SCRIPT)], cwd=target, env=environment,
                                text=True, capture_output=True, check=False)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def invalid_record(self, field, value):
        def mutate(target, path, record):
            record[field] = value
            path.write_text(json.dumps(record) + "\n")
        return self.fixture(mutate)

    def test_policy_refuses_a_foreign_repository(self):
        result = self.invalid_record("repository", "bijux-genomics")
        self.assertIn("exact Masterclass source authority", result.stderr)

    def test_policy_refuses_symbolic_source_reference(self):
        result = self.invalid_record("execution_policy_sha", "main")
        self.assertIn("exact Masterclass source authority", result.stderr)

    def test_policy_refuses_changed_programme_baseline(self):
        result = self.invalid_record("baseline_sha", "c" * 40)
        self.assertIn("exact Masterclass source authority", result.stderr)

    def test_policy_refuses_boolean_schema_alias(self):
        result = self.invalid_record("schema", True)
        self.assertIn("exact Masterclass source authority", result.stderr)

    def test_policy_refuses_untracked_authority(self):
        def mutate(target, path, record):
            subprocess.run(["git", "-C", str(target), "rm", "--cached", str(path.relative_to(target))], check=True, capture_output=True)
        result = self.fixture(mutate)
        self.assertIn("did not match any file", result.stderr)

    def test_policy_refuses_linked_authority(self):
        def mutate(target, path, record):
            outside = target / "authority.json"
            outside.write_bytes(path.read_bytes())
            path.unlink()
            path.symlink_to(outside)
        result = self.fixture(mutate)
        self.assertIn("regular workflow policy authority", result.stderr)

    def test_policy_refuses_linked_source_cache_before_fetch(self):
        def mutate(target, path, record):
            artifacts = target / "artifacts"
            artifacts.mkdir()
            unrelated = target / "unrelated"
            unrelated.mkdir()
            (artifacts / "github-policy-source").symlink_to(unrelated, target_is_directory=True)
        result = self.fixture(mutate)
        self.assertIn("workflow policy cache cannot contain symlinks", result.stderr)
