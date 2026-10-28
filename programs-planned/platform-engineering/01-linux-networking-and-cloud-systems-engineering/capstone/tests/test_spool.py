from __future__ import annotations

import os
import tempfile
import time
import unittest
from pathlib import Path

from atlas_host.spool import FileSpool


class SpoolTests(unittest.TestCase):
    def test_submit_claim_complete(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            spool = FileSpool(Path(raw))
            job_id = spool.submit({"text": "atlas"}, job_id="job_test")
            self.assertEqual(spool.status(job_id)["state"], "queued")
            claimed = spool.claim("worker-a")
            self.assertIsNotNone(claimed)
            assert claimed is not None
            self.assertEqual(claimed.job_id, job_id)
            result = spool.deterministic_result(claimed.payload)
            spool.complete(claimed, result)
            status = spool.status(job_id)
            self.assertEqual(status["state"], "completed")
            self.assertEqual(status["result"]["uppercase"], "ATLAS")

    def test_expired_claim_is_recovered(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            spool = FileSpool(Path(raw))
            spool.submit({"text": "recover"}, job_id="job_recover")
            claimed = spool.claim("worker-old")
            assert claimed is not None
            old = time.time() - 60
            os.utime(claimed.path, (old, old))
            self.assertEqual(spool.recover_expired(10), 1)
            self.assertEqual(spool.status("job_recover")["state"], "queued")

    def test_duplicate_job_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            spool = FileSpool(Path(raw))
            spool.submit({"text": "one"}, job_id="job_same")
            with self.assertRaises(FileExistsError):
                spool.submit({"text": "two"}, job_id="job_same")


if __name__ == "__main__":
    unittest.main()
