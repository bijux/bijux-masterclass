"""Cost per useful completed outcome."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .capacity import decimal


@dataclass(frozen=True, slots=True)
class UsefulCost:
    total_cost: Decimal
    useful_completions: Decimal
    cost_per_completion: Decimal


def cost_per_useful_completion(
    *,
    total_cost: Decimal,
    useful_completions: Decimal,
) -> UsefulCost:
    total_cost = decimal(total_cost)
    useful_completions = decimal(useful_completions)
    if total_cost < 0 or useful_completions <= 0:
        raise ValueError("cost must be non-negative and completions positive")
    return UsefulCost(
        total_cost=total_cost,
        useful_completions=useful_completions,
        cost_per_completion=total_cost / useful_completions,
    )
