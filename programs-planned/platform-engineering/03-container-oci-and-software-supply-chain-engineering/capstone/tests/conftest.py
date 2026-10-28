from __future__ import annotations

import sys
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
if str(CAPSTONE) not in sys.path:
    sys.path.insert(0, str(CAPSTONE))
