from __future__ import annotations

import stat
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(CAPSTONE_ROOT / "scripts"))

from execution_context import command_identity, repository_identity


class ExecutionContextTests(unittest.TestCase):
    def test_captures_resolved_tool_identity(self) -> None:
        with TemporaryDirectory() as directory:
            tool = Path(directory) / "compiler"
            tool.write_text(
                "#!/bin/sh\nprintf '%s\\n' 'Example Compiler 1.2' 'details'\n",
                encoding="utf-8",
            )
            tool.chmod(tool.stat().st_mode | stat.S_IXUSR)

            identity = command_identity(str(tool))

        self.assertEqual(identity["command"], str(tool))
        self.assertEqual(identity["executable"], str(tool.resolve()))
        self.assertEqual(identity["version"], "Example Compiler 1.2")

    def test_distinguishes_clean_and_dirty_repository_state(self) -> None:
        with TemporaryDirectory() as directory:
            repository = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
            subprocess.run(
                ["git", "config", "user.email", "learner@example.invalid"],
                cwd=repository,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Course Learner"],
                cwd=repository,
                check=True,
            )
            source = repository / "Makefile"
            source.write_text("all:\n\t@:\n", encoding="utf-8")
            subprocess.run(["git", "add", "Makefile"], cwd=repository, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "add build"],
                cwd=repository,
                check=True,
            )

            clean = repository_identity(repository)
            source.write_text("all:\n\t@echo changed\n", encoding="utf-8")
            dirty = repository_identity(repository)

        self.assertEqual(clean["status"], "clean")
        self.assertEqual(len(clean["revision"]), 40)
        self.assertEqual(dirty["revision"], clean["revision"])
        self.assertEqual(dirty["status"], "dirty")
        self.assertNotEqual(dirty["status_sha256"], clean["status_sha256"])

    def test_marks_non_repository_context_as_unavailable(self) -> None:
        with TemporaryDirectory() as directory:
            identity = repository_identity(Path(directory))

        self.assertEqual(identity["revision"], "unavailable")
        self.assertEqual(identity["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
