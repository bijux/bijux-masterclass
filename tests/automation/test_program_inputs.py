from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.program_qualification.inputs import program_inputs


class ProgramInputBoundaryTests(unittest.TestCase):
    def test_transitive_recipe_config_lock_workflow_modes_and_symlinks_are_bound(self):
        artifacts = (
            Path(__file__).resolve().parents[2]
            / "artifacts/program-admission/input-controls"
        )
        artifacts.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=artifacts) as directory:
            root = Path(directory)
            files = [
                "Makefile",
                "makes/root.mk",
                "configs/runtime.toml",
                ".github/workflows/program-validation.yml",
                "scripts/program_qualification/execute.py",
                ".bijux/shared/contract.py",
                "programs/family/course/capstone/src/library.py",
                "programs/family/course/capstone/requirements-tools.lock",
                "programs/family/course/course-book/index.md",
                "programs/family/other/capstone/src/library.py",
                "docs/index.md",
            ]
            for name in files:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(name)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            subprocess.run(["git", "add", "--", *files], cwd=root, check=True)
            original = program_inputs(root, "family/course")
            self.assertNotIn(files[-1], original)
            self.assertNotIn(files[-2], original)
            for name in files[:-2]:
                path = root / name
                prior = path.read_bytes()
                path.write_bytes(prior + b"changed")
                self.assertNotEqual(
                    program_inputs(root, "family/course"), original, name
                )
                path.write_bytes(prior)
            executable = root / files[4]
            executable.chmod(executable.stat().st_mode | 0o100)
            self.assertNotEqual(program_inputs(root, "family/course"), original)
            executable.chmod(executable.stat().st_mode & ~0o111)
            link = root / "programs/family/course/capstone/shared.py"
            link.symlink_to("../../../../.bijux/shared/contract.py")
            subprocess.run(["git", "add", "--", str(link)], cwd=root, check=True)
            linked = program_inputs(root, "family/course")
            (root / ".bijux/shared/contract.py").write_text(
                "changed transitive shared content"
            )
            self.assertNotEqual(program_inputs(root, "family/course"), linked)
            link.unlink()
            link.symlink_to(os.devnull)
            with self.assertRaises(ValueError):
                program_inputs(root, "family/course")


if __name__ == "__main__":
    unittest.main()
