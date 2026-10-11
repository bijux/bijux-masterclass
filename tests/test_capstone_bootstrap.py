"""Protect metadata toolchain ownership, child failures and immutable ready state."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CAPSTONE = ROOT / "programs/reproducible-research/deep-dive-snakemake/capstone"
spec = importlib.util.spec_from_file_location(
    "bootstrap_tools", CAPSTONE / "scripts/bootstrap_tools.py"
)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class CapstoneBootstrapTests(unittest.TestCase):
    """Execute the public preparation boundary using controlled tool children."""

    def setUp(self):
        directory = ROOT / "artifacts/capstone-toolchain/controls"
        directory.mkdir(parents=True, exist_ok=True)
        fixture = tempfile.TemporaryDirectory(dir=directory)
        self.addCleanup(fixture.cleanup)
        self.root = Path(fixture.name)
        self.capstone = self.root / "capstone"
        self.capstone.mkdir()
        for name in (
            "pyproject.toml",
            "requirements-tools.lock",
            "requirements-tools.provenance.json",
            "Makefile",
            "scripts/bootstrap_tools.py",
        ):
            destination = self.capstone / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(CAPSTONE / name, destination)
        self.python = self.root / "base-python"
        self.python.write_bytes(b"controlled interpreter")
        self.uv = self.root / "uv"
        self.uv.write_bytes(b"controlled installer")
        self.target = self.root / "artifacts/venv/tools"
        self.receipt = self.root / "artifacts/proof/toolchain.json"
        self.runtime = {
            "implementation": "CPython",
            "version": "3.11.13",
            "system": "Darwin",
            "machine": "arm64",
            "prefix": str(self.root / "base"),
            "base_prefix": str(self.root / "base"),
        }
        self.calls = []
        self.failure = None
        self.installed_drift = False
        self.source_drift = False
        tools = patch.object(
            bootstrap.shutil,
            "which",
            side_effect=lambda name: str(
                self.python if name == "python-selected" else self.uv
            ),
        )
        tools.start()
        self.addCleanup(tools.stop)
        child = patch.object(bootstrap, "run", side_effect=self.command)
        child.start()
        self.addCleanup(child.stop)

    def command(self, args, environment):
        self.calls.append(args)
        self.assertEqual(environment["UV_PYTHON_DOWNLOADS"], "never")
        self.assertTrue(
            Path(environment["UV_CACHE_DIR"]).is_relative_to(self.root / "artifacts")
        )
        if self.failure and self.failure in args:
            raise RuntimeError("controlled child failure")
        if args[-1] == bootstrap.RUNTIME:
            return json.dumps(
                {
                    **self.runtime,
                    "prefix": self.runtime["prefix"]
                    if args[0] == str(self.python)
                    else str(self.target),
                }
            )
        if "--version" in args:
            return "uv 0.11.17" if args[0] == str(self.uv) else "controlled locked tool"
        if "venv" in args:
            (self.target / "bin").mkdir()
            (self.target / "bin/python").symlink_to(self.python)
            self.assertIn("--without-pip", args)
            return ""
        if "sync" in args:
            self.assertIn("--require-hashes", args)
            return ""
        if bootstrap.CLOSURE in args:
            if self.installed_drift:
                raise RuntimeError(
                    "Installed closure differs from the exact platform lock"
                )
            if self.source_drift:
                source = self.capstone / "Makefile"
                source.write_bytes(source.read_bytes() + b"\n# changed recipe\n")
            return json.dumps(
                {"packages": {"snakemake": "9.27.0"}, "runtime": self.runtime}
            )
        if "check" in args:
            return ""
        if "import importlib.metadata" in args[-1]:
            return "[]"
        raise AssertionError(args)

    def prepare(self, **kwargs):
        return bootstrap.prepare(
            self.root,
            self.capstone,
            "python-selected",
            self.target,
            "uv-selected",
            self.receipt,
            **kwargs,
        )

    def test_fresh_install_and_ready_revalidation_preserve_exact_identity(self):
        result = self.prepare()
        self.assertEqual(result["status"], "ready")
        marker = (self.target / bootstrap.MARKER).read_bytes()
        self.calls.clear()
        self.assertEqual(self.prepare(), result)
        self.assertFalse(any("venv" in args or "sync" in args for args in self.calls))
        self.assertEqual((self.target / bootstrap.MARKER).read_bytes(), marker)

    def test_fresh_confirmation_refuses_reusing_an_existing_environment(self):
        self.prepare()
        self.calls.clear()
        with self.assertRaisesRegex(RuntimeError, "new artifact environment"):
            self.prepare(fresh=True)
        self.assertFalse(any("venv" in args or "sync" in args for args in self.calls))

    def test_metadata_drift_requires_a_new_reviewed_lock(self):
        metadata = self.capstone / "pyproject.toml"
        metadata.write_bytes(metadata.read_bytes() + b"\n# owner changed\n")
        with self.assertRaisesRegex(RuntimeError, "current package metadata"):
            self.prepare()
        self.assertFalse(self.target.exists())
        self.assertEqual(self.calls, [])

    def test_stale_recipe_preserves_ready_environment(self):
        self.prepare()
        marker = (self.target / bootstrap.MARKER).read_bytes()
        recipe = self.capstone / "Makefile"
        recipe.write_bytes(recipe.read_bytes() + b"\n# owner changed\n")
        with self.assertRaisesRegex(RuntimeError, "stale tool environment"):
            self.prepare()
        self.assertEqual((self.target / bootstrap.MARKER).read_bytes(), marker)

    def test_installed_package_drift_is_never_resynchronized(self):
        self.prepare()
        self.installed_drift = True
        self.calls.clear()
        with self.assertRaisesRegex(RuntimeError, "Installed closure"):
            self.prepare()
        self.assertFalse(any("sync" in args for args in self.calls))

    def test_failed_installer_never_creates_a_ready_marker(self):
        self.failure = "sync"
        with self.assertRaisesRegex(RuntimeError, "child failure"):
            self.prepare()
        self.assertEqual(
            json.loads((self.target / bootstrap.MARKER).read_text())["status"],
            "preparing",
        )
        self.assertFalse(self.receipt.exists())

    def test_unowned_or_outside_or_aliased_environment_preserves_user_bytes(self):
        self.target.mkdir(parents=True)
        sentinel = self.target / "user-data"
        sentinel.write_bytes(b"user bytes")
        with self.assertRaisesRegex(RuntimeError, "unowned"):
            self.prepare()
        self.assertEqual(sentinel.read_bytes(), b"user bytes")
        outside = self.root / "outside"
        outside.mkdir()
        self.target = outside
        with self.assertRaisesRegex(RuntimeError, "inside repository artifacts"):
            self.prepare()
        link = self.root / "artifacts/link"
        link.symlink_to(outside, target_is_directory=True)
        self.target = link / "tools"
        with self.assertRaisesRegex(RuntimeError, "aliases"):
            self.prepare()
        self.assertFalse(list(outside.iterdir()))

    def test_unsupported_or_nonbase_runtime_is_refused_before_environment_creation(
        self,
    ):
        original = self.runtime.copy()
        for changes in (
            {"version": "3.10.9"},
            {"implementation": "PyPy"},
            {"prefix": str(self.root / "venv")},
        ):
            self.runtime = {**original, **changes}
            with (
                self.subTest(changes=changes),
                self.assertRaisesRegex(RuntimeError, "supported base CPython"),
            ):
                self.prepare()
            self.assertFalse(self.target.exists())

    def test_source_mutation_during_install_refuses_ready_admission(self):
        self.source_drift = True
        with self.assertRaisesRegex(RuntimeError, "source changed"):
            self.prepare()
        self.assertEqual(
            json.loads((self.target / bootstrap.MARKER).read_text())["status"],
            "preparing",
        )
        self.assertFalse(self.receipt.exists())

    def test_duplicate_marker_identity_is_refused_without_mutation(self):
        self.prepare()
        marker = self.target / bootstrap.MARKER
        marker.write_text('{"schema":1,"schema":1}')
        before = marker.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "Duplicate"):
            self.prepare()
        self.assertEqual(marker.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
