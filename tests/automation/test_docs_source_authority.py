from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]


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
            ["bash", "scripts/verify_docs_source.sh"], cwd=ROOT,
            env=dict(os.environ, BIJUX_STD_REF="0" * 40),
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("override differs from the declared source pin", result.stderr)

    def test_unknown_source_mode_is_refused(self) -> None:
        result = subprocess.run(
            ["bash", "scripts/verify_docs_source.sh", "foreign-mode"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mode must be check or sync", result.stderr)
