from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from atlas_host.atomic_store import atomic_write_bytes, atomic_write_json, read_json


class AtomicStoreTests(unittest.TestCase):
    def test_atomic_bytes_replace_and_leave_no_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target = root / "value.bin"
            atomic_write_bytes(target, b"first")
            atomic_write_bytes(target, b"second")
            self.assertEqual(target.read_bytes(), b"second")
            self.assertEqual([p for p in root.iterdir() if p.name.startswith(".value.bin.")], [])

    def test_json_is_canonical_and_readable(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "value.json"
            atomic_write_json(path, {"z": 1, "a": [2, 3]})
            self.assertEqual(path.read_text(), '{"a":[2,3],"z":1}\n')
            self.assertEqual(read_json(path), {"a": [2, 3], "z": 1})


if __name__ == "__main__":
    unittest.main()
