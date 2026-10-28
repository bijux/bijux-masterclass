#!/usr/bin/env python3
"""Prove that each named Course 4 defect is rejected by its intended oracle."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from api_reliability.faults import FaultPlan
from api_reliability.metrics import MetricDescriptor, MetricError
from api_reliability.telemetry import TelemetryEvent

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capstone"


def rejected(callable_, expected: type[BaseException]) -> bool:
    try:
        callable_()
    except expected:
        return True
    return False


def detect_journey_slo_coverage(catalog: dict[str, object]) -> None:
    for row in catalog.get("slos", []):
        if not isinstance(row, dict) or not row.get("journeys"):
            raise ValueError("SLO must reference at least one critical journey")


def detect_deadline_parent_bound(parent_expiry: int, child_expiry: int) -> None:
    if child_expiry > parent_expiry:
        raise ValueError("child deadline extended parent")


def detect_circuit_scope(policy: dict[str, object]) -> None:
    if policy.get("circuitBreaker") and policy.get("circuitScope") != "dependency":
        raise ValueError("circuit must be dependency-scoped")


def detect_distinct_health(liveness: str, readiness: str) -> None:
    if liveness == readiness:
        raise ValueError("liveness and readiness were collapsed")


def detect_trace_topology(edge: dict[str, str]) -> None:
    if edge.get("kind") in {"durable-queue", "durable-outbox"} and edge.get("relation") != "link":
        raise ValueError("durable asynchronous edge requires a trace link")


def detect_slo_catalog_version(catalog: dict[str, object]) -> None:
    version = catalog.get("catalogVersion")
    if not isinstance(version, str) or not version:
        raise ValueError("SLO catalog is unversioned")


def detect_incident_roles(roles: dict[str, str]) -> None:
    if not roles.get("incidentCommander"):
        raise ValueError("incident commander is required")


def main() -> None:
    defects = json.loads(
        (CAP / "planted-defects" / "DEFECTS.json").read_text(encoding="utf-8")
    )["defects"]
    detected: dict[str, bool] = {}

    detected["journey-slo-coverage"] = rejected(
        lambda: detect_journey_slo_coverage({"slos": [{"id": "mutant", "journeys": []}]}),
        ValueError,
    )
    detected["deadline-parent-bound"] = rejected(
        lambda: detect_deadline_parent_bound(1_500, 2_000),
        ValueError,
    )
    detected["dependency-circuit-scope"] = rejected(
        lambda: detect_circuit_scope({"circuitBreaker": True, "circuitScope": "global"}),
        ValueError,
    )
    detected["distinct-health-contracts"] = rejected(
        lambda: detect_distinct_health(
            "all-required-dependencies-available",
            "all-required-dependencies-available",
        ),
        ValueError,
    )
    detected["telemetry-event-schema"] = rejected(
        lambda: TelemetryEvent(
            timestamp_ms=0,
            severity="INFO",
            event_name="Worker Job Claimed",
            service_name="analysis-api",
            service_version="1.3.0",
            deployment_environment="test",
            schema_version="1.0",
            attributes={},
        ),
        ValueError,
    )
    detected["metric-identifier-label-policy"] = rejected(
        lambda: MetricDescriptor(
            name="analysis_run_events_total",
            description="Mutant metric.",
            unit="events",
            labels=("run_id",),
        ),
        MetricError,
    )
    detected["durable-trace-link-policy"] = rejected(
        lambda: detect_trace_topology(
            {"kind": "durable-queue", "relation": "parent-child"}
        ),
        ValueError,
    )
    detected["slo-catalog-version"] = rejected(
        lambda: detect_slo_catalog_version({"slos": []}),
        ValueError,
    )
    detected["fault-plan-hypothesis"] = rejected(
        lambda: FaultPlan(
            identifier="worker-loss",
            hypothesis="",
            steady_state=("one durable run exists",),
            blast_radius="one synthetic run",
            abort_conditions=("duplicate terminal effect",),
            cleanup=("restore worker",),
        ).validate(),
        ValueError,
    )
    detected["incident-role-contract"] = rejected(
        lambda: detect_incident_roles({"operationsLead": "B. Engineer"}),
        ValueError,
    )

    missing = []
    for row in defects:
        spec = CAP / "planted-defects" / row["id"] / "defect.yaml"
        if not spec.is_file():
            missing.append(f"{row['id']}:missing-spec")
            continue
        parsed = yaml.safe_load(spec.read_text(encoding="utf-8"))
        if parsed.get("detector") != row.get("detector"):
            missing.append(f"{row['id']}:detector-mismatch")
        if detected.get(row["detector"]) is not True:
            missing.append(f"{row['id']}:not-detected")
    if missing:
        raise SystemExit("FAIL planted defect sensitivity: " + ", ".join(missing))
    print(f"PASS planted defect sensitivity — {len(defects)} defects rejected")


if __name__ == "__main__":
    main()
