from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path

from atlas_host.health import worker_heartbeat, writable_directory


class HealthTests(unittest.TestCase):
    def test_writable_directory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            ok, detail = writable_directory(Path(raw) / "state")
            self.assertTrue(ok)
            self.assertEqual(detail, "writable")

    def test_heartbeat_missing_and_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            runtime = Path(raw)
            self.assertFalse(worker_heartbeat(runtime)[0])
            (runtime / "worker.heartbeat").write_text(str(time.time_ns()))
            self.assertTrue(worker_heartbeat(runtime)[0])


if __name__ == "__main__":
    unittest.main()
