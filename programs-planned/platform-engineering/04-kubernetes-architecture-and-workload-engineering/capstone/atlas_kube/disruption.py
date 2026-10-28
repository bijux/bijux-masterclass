from __future__ import annotations

import math
import re


def _resolve(value: int | str, desired: int, *, round_up: bool) -> int:
    if isinstance(value, int):
        return value
    m = re.fullmatch(r"(\d+)%", value)
    if not m:
        raise ValueError("invalid percentage")
    raw = desired * int(m.group(1)) / 100
    return math.ceil(raw) if round_up else math.floor(raw)


def disruptions_allowed(*, desired: int, healthy: int,
                        min_available: int | str | None = None,
                        max_unavailable: int | str | None = None) -> int:
    if (min_available is None) == (max_unavailable is None):
        raise ValueError("set exactly one of min_available or max_unavailable")
    if min_available is not None:
        required = _resolve(min_available, desired, round_up=True)
    else:
        unavailable = _resolve(max_unavailable, desired, round_up=True)
        required = max(0, desired - unavailable)
    return max(0, healthy - required)
