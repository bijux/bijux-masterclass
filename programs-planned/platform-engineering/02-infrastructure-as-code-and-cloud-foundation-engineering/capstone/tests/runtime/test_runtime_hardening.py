from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from atlas_host.config import AtlasConfig, ConfigError
from atlas_host.health import writable_directory
from atlas_host.spool import FileSpool


class RuntimeHardeningTests(unittest.TestCase):
    def test_config_rejects_relative_and_overlapping_directories(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "bad.json"
            path.write_text(json.dumps({
                "runtimeDir": "relative",
                "stateDir": str(root / "state"),
                "logDir": str(root / "log"),
            }))
            with self.assertRaises(ConfigError):
                AtlasConfig.from_json(path)

            path.write_text(json.dumps({
                "runtimeDir": str(root / "same"),
                "stateDir": str(root / "same"),
                "logDir": str(root / "log"),
            }))
            with self.assertRaises(ConfigError):
                AtlasConfig.from_json(path)

    def test_readiness_probe_cleans_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            ok, _ = writable_directory(root)
            self.assertTrue(ok)
            self.assertEqual([], list(root.iterdir()))

    def test_recovery_reconciles_published_result(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            spool = FileSpool(Path(raw))
            job_id = spool.submit({"text": "x"})
            claimed = spool.claim("worker-a")
            assert claimed is not None
            # Simulate a crash after result publication but before processing cleanup.
            from atlas_host.atomic_store import atomic_write_json
            atomic_write_json(spool.results / f"{job_id}.json", {"jobId": job_id, "result": {"ok": True}})
            claimed.path.touch()
            count = spool.recover_expired(0)
            self.assertEqual(1, count)
            self.assertFalse(claimed.path.exists())
            self.assertFalse((spool.queued / f"{job_id}.json").exists())
            self.assertEqual("completed", spool.status(job_id)["state"])


if __name__ == "__main__":
    unittest.main()
