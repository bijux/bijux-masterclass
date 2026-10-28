"""Database connection and query budget arithmetic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConnectionBudget:
    api_instances: int
    api_pool_max: int
    workers: int
    worker_pool_max: int
    operational_reserve: int

    def __post_init__(self) -> None:
        if any(
            value < 0
            for value in (
                self.api_instances,
                self.api_pool_max,
                self.workers,
                self.worker_pool_max,
                self.operational_reserve,
            )
        ):
            raise ValueError("connection budget values must be non-negative")

    @property
    def possible_connections(self) -> int:
        return (
            self.api_instances * self.api_pool_max
            + self.workers * self.worker_pool_max
            + self.operational_reserve
        )

    def fits(self, database_max_connections: int) -> bool:
        if database_max_connections <= 0:
            raise ValueError("database maximum must be positive")
        return self.possible_connections <= database_max_connections


def pool_utilization(active: int, maximum: int) -> float:
    if maximum <= 0 or active < 0 or active > maximum:
        raise ValueError("invalid pool values")
    return active / maximum
