from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from atlas_host.config import AtlasConfig


class ConfigTests(unittest.TestCase):
    def test_config_prepares_required_directories(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "atlas.json"
            path.write_text(json.dumps({
                "runtimeDir": str(root / "run"),
                "stateDir": str(root / "state"),
                "logDir": str(root / "log"),
                "apiPort": 0,
                "edgePort": 0
            }))
            config = AtlasConfig.from_json(path)
            config.prepare()
            self.assertTrue((root / "state" / "spool" / "queued").is_dir())
            self.assertTrue((root / "log").is_dir())


if __name__ == "__main__":
    unittest.main()
