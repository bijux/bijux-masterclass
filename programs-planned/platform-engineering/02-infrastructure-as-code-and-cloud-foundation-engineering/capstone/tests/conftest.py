from __future__ import annotations

import sys
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
for path in (CAPSTONE, CAPSTONE / "runtime"):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)
