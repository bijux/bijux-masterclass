from __future__ import annotations

from dataclasses import dataclass
import math
import re


@dataclass(frozen=True, slots=True)
class RolloutBounds:
    replicas: int
    max_surge: int
    max_unavailable: int
    max_total: int
    min_available: int


def resolve_int_or_percent(value: int | str, replicas: int, *, round_up: bool) -> int:
    if isinstance(value, int):
        if value < 0:
            raise ValueError("value must be non-negative")
        return value
    match = re.fullmatch(r"(\d+)%", value)
    if not match:
        raise ValueError(f"invalid IntOrString value: {value!r}")
    raw = replicas * int(match.group(1)) / 100
    return math.ceil(raw) if round_up else math.floor(raw)


def rollout_bounds(replicas: int, max_surge: int | str,
                   max_unavailable: int | str) -> RolloutBounds:
    if replicas < 0:
        raise ValueError("replicas must be non-negative")
    surge = resolve_int_or_percent(max_surge, replicas, round_up=True)
    unavailable = resolve_int_or_percent(max_unavailable, replicas, round_up=False)
    if replicas > 0 and surge == 0 and unavailable == 0:
        raise ValueError("surge and unavailable cannot both resolve to zero")
    return RolloutBounds(
        replicas=replicas,
        max_surge=surge,
        max_unavailable=unavailable,
        max_total=replicas + surge,
        min_available=max(0, replicas - unavailable),
    )


def rollout_complete(*, desired: int, updated: int, ready: int, available: int,
                     unavailable: int) -> bool:
    return (
        updated == desired
        and ready == desired
        and available == desired
        and unavailable == 0
    )
