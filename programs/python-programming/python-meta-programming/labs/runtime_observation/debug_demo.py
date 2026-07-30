from __future__ import annotations

import json

from .debug_view import build_debug_view
from .evidence import IncidentObservationTarget


def main() -> int:
    target = IncidentObservationTarget("queue lag")
    payload = [entry.as_dict() for entry in build_debug_view(target)]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
