from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.program_qualification.execute import run
from scripts.program_qualification.github import find_saved_qualification, read_receipt
from scripts.program_qualification.inputs import runtime_inputs


class ProgramExecutionBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.artifacts = (
            Path(__file__).resolve().parents[2]
            / "artifacts/program-admission/execution-controls"
        )
        self.artifacts.mkdir(parents=True, exist_ok=True)

    def test_child_status_is_not_masked_by_log_publication(self):
        with TemporaryDirectory(dir=self.artifacts) as directory:
            log = Path(directory) / "child.log"
            run(
                [sys.executable, "-c", 'print("executed")'],
                cwd=Path(directory),
                env=dict(os.environ),
                log=log,
            )
            self.assertEqual(log.read_text().strip(), "executed")
            with self.assertRaises(subprocess.CalledProcessError) as failure:
                run(
                    [sys.executable, "-c", 'print("refusal");raise SystemExit(7)'],
                    cwd=Path(directory),
                    env=dict(os.environ),
                    log=log,
                )
            self.assertEqual(failure.exception.returncode, 7)
            self.assertEqual(log.read_text().strip(), "refusal")

    def test_artifact_is_digest_checked_bounded_data_without_extraction(self):
        def archive(entries):
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, "w") as bundle:
                for name, value in entries.items():
                    bundle.writestr(name, value)
            return stream.getvalue()

        valid = archive({"qualification.json": json.dumps({"result": "success"})})
        metadata = {
            "id": 1,
            "expired": False,
            "size_in_bytes": len(valid),
            "digest": "sha256:" + hashlib.sha256(valid).hexdigest(),
        }
        with patch(
            "scripts.program_qualification.github.subprocess.check_output",
            return_value=valid,
        ):
            self.assertEqual(read_receipt(metadata), {"result": "success"})
            with self.assertRaises(ValueError):
                read_receipt(dict(metadata, digest="sha256:incorrect"))
        for contents in (
            {"../code.py": "raise SystemExit(0)"},
            {"qualification.json": "{}", "code.py": "pass"},
            {"qualification.json": "[]"},
        ):
            raw = archive(contents)
            wrong = dict(
                metadata,
                digest="sha256:" + hashlib.sha256(raw).hexdigest(),
                size_in_bytes=len(raw),
            )
            with (
                self.subTest(contents=contents),
                patch(
                    "scripts.program_qualification.github.subprocess.check_output",
                    return_value=raw,
                ),
                self.assertRaises((ValueError, TypeError)),
            ):
                read_receipt(wrong)
        with patch(
            "scripts.program_qualification.github.api", side_effect=OSError("offline")
        ):
            self.assertIsNone(
                find_saved_qualification(
                    self.artifacts, {"dependencies_locked": True}, "qualification"
                )
            )
        with patch("scripts.program_qualification.github.api") as api:
            self.assertIsNone(
                find_saved_qualification(
                    self.artifacts, {"dependencies_locked": False}, "qualification"
                )
            )
            api.assert_not_called()

    def test_same_version_installed_payload_mutation_changes_runtime_identity(self):
        with TemporaryDirectory(dir=self.artifacts) as directory:
            environment = Path(directory) / "venv"
            subprocess.run(
                [sys.executable, "-m", "venv", "--without-pip", str(environment)],
                check=True,
            )
            python = environment / "bin/python"
            site = Path(
                subprocess.check_output(
                    [
                        str(python),
                        "-c",
                        'import sysconfig;print(sysconfig.get_path("purelib"))',
                    ],
                    text=True,
                ).strip()
            )
            metadata = site / "bijux_probe-1.0.dist-info"
            metadata.mkdir()
            (metadata / "METADATA").write_text(
                "Metadata-Version: 2.1\nName: bijux-probe\nVersion: 1.0\n"
            )
            (metadata / "RECORD").write_text(
                "bijux_probe.py,,\nbijux_probe-1.0.dist-info/METADATA,,\nbijux_probe-1.0.dist-info/RECORD,,\n"
            )
            payload = site / "bijux_probe.py"
            payload.write_text("value = 1\n")
            prior = runtime_inputs(python)
            payload.write_text("value = 2\n")
            observed = runtime_inputs(python)
            self.assertEqual(
                prior["packages"][0]["version"], observed["packages"][0]["version"]
            )
            self.assertNotEqual(prior, observed)
            payload.unlink()
            with self.assertRaises(subprocess.CalledProcessError):
                runtime_inputs(python)
            (metadata / "RECORD").unlink()
            (metadata / "SOURCES.txt").write_text("bijux_probe.py\n")
            legacy = runtime_inputs(python)
            self.assertFalse(legacy["packages"][0]["installed_record"])
            self.assertEqual(
                legacy["packages"][0]["files"]["bijux_probe.py"],
                "legacy source manifest; not installed payload",
            )


if __name__ == "__main__":
    unittest.main()
