from __future__ import annotations

import sys
from pathlib import Path

# Make the repository root importable so tests can do `import capstone.*`.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
