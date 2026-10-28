"""Auditable capacity arithmetic using Decimal."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Mapping


def decimal(value: str | int | Decimal) -> Decimal:
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("invalid decimal") from exc
    if not result.is_finite():
        raise ValueError("decimal must be finite")
    return result


def cpu_demand(
    *,
    cores: Decimal,
    utilization: Decimal,
    interval_seconds: Decimal,
    completions: Decimal,
) -> Decimal:
    values = tuple(map(decimal, (cores, utilization, interval_seconds, completions)))
    cores, utilization, interval_seconds, completions = values
    if cores <= 0 or interval_seconds <= 0 or completions <= 0:
        raise ValueError("capacity inputs must be positive")
    if not Decimal("0") <= utilization <= Decimal("1"):
        raise ValueError("utilization must be in [0, 1]")
    return (cores * utilization * interval_seconds) / completions


def utilization_from_demand(
    *,
    arrival_rate: Decimal,
    demand_per_completion: Decimal,
    capacity_units: Decimal,
) -> Decimal:
    arrival_rate = decimal(arrival_rate)
    demand_per_completion = decimal(demand_per_completion)
    capacity_units = decimal(capacity_units)
    if arrival_rate < 0 or demand_per_completion < 0 or capacity_units <= 0:
        raise ValueError("invalid utilization inputs")
    return arrival_rate * demand_per_completion / capacity_units


def backlog_drain_seconds(
    *,
    backlog: Decimal,
    completion_rate: Decimal,
    arrival_rate: Decimal,
) -> Decimal:
    backlog = decimal(backlog)
    completion_rate = decimal(completion_rate)
    arrival_rate = decimal(arrival_rate)
    if backlog < 0 or completion_rate < 0 or arrival_rate < 0:
        raise ValueError("rates and backlog must be non-negative")
    surplus = completion_rate - arrival_rate
    if surplus <= 0:
        raise ValueError("backlog cannot drain when completion <= arrival")
    return backlog / surplus


@dataclass(frozen=True, slots=True)
class WorkloadDemand:
    id: str
    rate_per_second: Decimal
    resource_demand: Mapping[str, Decimal]

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("workload id is required")
        if decimal(self.rate_per_second) < 0:
            raise ValueError("rate cannot be negative")
        if any(decimal(value) < 0 for value in self.resource_demand.values()):
            raise ValueError("resource demand cannot be negative")


@dataclass(frozen=True, slots=True)
class ResourceCapacity:
    id: str
    capacity_units: Decimal
    target_utilization: Decimal
    cost_per_hour: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if not self.id or decimal(self.capacity_units) <= 0:
            raise ValueError("resource capacity must be positive")
        target = decimal(self.target_utilization)
        if not Decimal("0") < target <= Decimal("1"):
            raise ValueError("target utilization must be in (0, 1]")


@dataclass(frozen=True, slots=True)
class ResourceResult:
    id: str
    utilization: Decimal
    target_utilization: Decimal
    headroom_fraction: Decimal
    within_target: bool


@dataclass(frozen=True, slots=True)
class CapacityResult:
    resources: tuple[ResourceResult, ...]
    first_bottleneck: str | None


def evaluate_capacity(
    workloads: tuple[WorkloadDemand, ...],
    resources: tuple[ResourceCapacity, ...],
) -> CapacityResult:
    results: list[ResourceResult] = []
    for resource in resources:
        total = Decimal("0")
        for workload in workloads:
            demand = decimal(workload.resource_demand.get(resource.id, Decimal("0")))
            total += decimal(workload.rate_per_second) * demand
        utilization = total / decimal(resource.capacity_units)
        target = decimal(resource.target_utilization)
        headroom = (
            (target - utilization) / target
            if target > 0
            else Decimal("-Infinity")
        )
        results.append(
            ResourceResult(
                id=resource.id,
                utilization=utilization,
                target_utilization=target,
                headroom_fraction=headroom,
                within_target=utilization <= target,
            )
        )
    ordered = sorted(
        results,
        key=lambda item: (
            item.utilization / item.target_utilization,
            item.id,
        ),
        reverse=True,
    )
    first = ordered[0].id if ordered else None
    return CapacityResult(tuple(results), first)


def storage_bytes(
    *,
    daily_objects: Decimal,
    mean_object_bytes: Decimal,
    retention_days: Decimal,
    replication_factor: Decimal = Decimal("1"),
    overhead_fraction: Decimal = Decimal("0"),
) -> Decimal:
    values = tuple(
        map(
            decimal,
            (
                daily_objects,
                mean_object_bytes,
                retention_days,
                replication_factor,
                overhead_fraction,
            ),
        )
    )
    daily_objects, mean_object_bytes, retention_days, replication_factor, overhead = values
    if min(daily_objects, mean_object_bytes, retention_days) < 0:
        raise ValueError("storage inputs must be non-negative")
    if replication_factor <= 0 or overhead < 0:
        raise ValueError("invalid storage multipliers")
    base = daily_objects * mean_object_bytes * retention_days
    return base * replication_factor * (Decimal("1") + overhead)
