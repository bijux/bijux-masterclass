"""Parse the capstone performance experiment policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SUPPORTED_STATES = frozenset({"clean", "converged"})
SUPPORTED_ROUTES = frozenset({"all", "dry-run-all"})


@dataclass(frozen=True)
class PerformanceScenario:
    name: str
    state: str
    jobs: int
    route: str


def read_performance_policy(policy_path: Path) -> list[PerformanceScenario]:
    """Return validated scenarios in policy order."""
    scenarios: list[PerformanceScenario] = []
    names: set[str] = set()

    for line_number, raw_line in enumerate(
        policy_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line or raw_line.startswith("#"):
            continue

        fields = raw_line.split("\t")
        if len(fields) != 4:
            raise ValueError(
                f"line {line_number}: expected scenario, state, jobs, and route"
            )

        name, state, raw_jobs, route = fields
        if (
            not name
            or not name[0].islower()
            or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-" for character in name)
        ):
            raise ValueError(f"line {line_number}: invalid scenario name: {name!r}")
        if name in names:
            raise ValueError(f"line {line_number}: duplicate scenario: {name}")
        if state not in SUPPORTED_STATES:
            raise ValueError(f"line {line_number}: unsupported state: {state!r}")
        if route not in SUPPORTED_ROUTES:
            raise ValueError(f"line {line_number}: unsupported route: {route!r}")
        try:
            jobs = int(raw_jobs)
        except ValueError as error:
            raise ValueError(
                f"line {line_number}: jobs must be a positive integer"
            ) from error
        if jobs < 1:
            raise ValueError(f"line {line_number}: jobs must be a positive integer")

        names.add(name)
        scenarios.append(PerformanceScenario(name, state, jobs, route))

    if not scenarios:
        raise ValueError("performance policy contains no scenarios")
    return scenarios
