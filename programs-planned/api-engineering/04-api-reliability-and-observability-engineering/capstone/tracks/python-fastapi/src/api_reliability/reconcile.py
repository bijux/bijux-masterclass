from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum


class FindingKind(str, Enum):
    RUN_WITHOUT_JOB = "run-without-job"
    JOB_WITHOUT_RUN = "job-without-run"
    TERMINAL_JOB_NONTERMINAL_RUN = "terminal-job-nonterminal-run"
    TERMINAL_RUN_NONTERMINAL_JOB = "terminal-run-nonterminal-job"
    COMPLETED_RUN_MISSING_ARTIFACT = "completed-run-missing-artifact"
    MULTIPLE_ARTIFACTS = "multiple-artifacts"
    ARTIFACT_WITHOUT_COMPLETED_RUN = "artifact-without-completed-run"
    TERMINAL_RUN_MISSING_OUTBOX = "terminal-run-missing-outbox"
    DUPLICATE_TERMINAL_OUTBOX = "duplicate-terminal-outbox"
    TERMINAL_RUN_MISSING_EVENT = "terminal-run-missing-event"
    DUPLICATE_TERMINAL_EVENT = "duplicate-terminal-event"


@dataclass(frozen=True, slots=True)
class RunRow:
    run_id: str
    status: str


@dataclass(frozen=True, slots=True)
class JobRow:
    run_id: str
    status: str


@dataclass(frozen=True, slots=True)
class ArtifactRow:
    run_id: str
    artifact_id: str


@dataclass(frozen=True, slots=True)
class OutboxRow:
    run_id: str
    event_type: str


@dataclass(frozen=True, slots=True)
class EventRow:
    run_id: str
    status: str


@dataclass(frozen=True, slots=True)
class Finding:
    kind: FindingKind
    run_id: str
    repair_key: str
    detail: str


@dataclass(frozen=True, slots=True)
class Snapshot:
    runs: tuple[RunRow, ...]
    jobs: tuple[JobRow, ...]
    artifacts: tuple[ArtifactRow, ...]
    outbox: tuple[OutboxRow, ...]
    events: tuple[EventRow, ...] = ()


_RUN_TERMINAL = frozenset({"completed", "failed", "canceled"})
_JOB_TERMINAL = frozenset({"completed", "dead", "canceled"})
_OUTBOX_EXPECTED = {
    "completed": "analysis.completed",
    "failed": "analysis.failed",
}


def inspect(snapshot: Snapshot) -> tuple[Finding, ...]:
    """Return read-only, deterministic cross-table consistency findings.

    The inspector never repairs data and never chooses truth when sources
    disagree. ``repair_key`` only makes a separately reviewed repair idempotent.
    """

    runs = {row.run_id: row for row in snapshot.runs}
    jobs = {row.run_id: row for row in snapshot.jobs}
    artifacts: dict[str, list[ArtifactRow]] = defaultdict(list)
    outbox: dict[str, list[OutboxRow]] = defaultdict(list)
    events: dict[str, list[EventRow]] = defaultdict(list)
    for row in snapshot.artifacts:
        artifacts[row.run_id].append(row)
    for row in snapshot.outbox:
        outbox[row.run_id].append(row)
    for row in snapshot.events:
        events[row.run_id].append(row)

    findings: list[Finding] = []
    for run_id in sorted(set(runs) | set(jobs) | set(artifacts) | set(outbox) | set(events)):
        run = runs.get(run_id)
        job = jobs.get(run_id)
        run_artifacts = artifacts.get(run_id, [])
        run_outbox = outbox.get(run_id, [])
        run_events = events.get(run_id, [])

        if run is None and job is not None:
            findings.append(_finding(FindingKind.JOB_WITHOUT_RUN, run_id))
            continue
        if run is None:
            # Foreign keys should prevent these rows in the reference schema.
            # They are still surfaced if a forensic snapshot contains them.
            if run_artifacts:
                findings.append(
                    _finding(FindingKind.ARTIFACT_WITHOUT_COMPLETED_RUN, run_id)
                )
            continue

        if run.status in {"queued", "running"} and job is None:
            findings.append(_finding(FindingKind.RUN_WITHOUT_JOB, run_id))
        if job and job.status in _JOB_TERMINAL and run.status not in _RUN_TERMINAL:
            findings.append(
                _finding(FindingKind.TERMINAL_JOB_NONTERMINAL_RUN, run_id)
            )
        if job and run.status in _RUN_TERMINAL and job.status not in _JOB_TERMINAL:
            findings.append(
                _finding(FindingKind.TERMINAL_RUN_NONTERMINAL_JOB, run_id)
            )

        if run.status == "completed" and not run_artifacts:
            findings.append(
                _finding(FindingKind.COMPLETED_RUN_MISSING_ARTIFACT, run_id)
            )
        if len(run_artifacts) > 1:
            findings.append(_finding(FindingKind.MULTIPLE_ARTIFACTS, run_id))
        if run_artifacts and run.status != "completed":
            findings.append(
                _finding(FindingKind.ARTIFACT_WITHOUT_COMPLETED_RUN, run_id)
            )

        expected_outbox = _OUTBOX_EXPECTED.get(run.status)
        matching_outbox = [
            row for row in run_outbox if row.event_type == expected_outbox
        ] if expected_outbox else []
        if expected_outbox and not matching_outbox:
            findings.append(
                _finding(FindingKind.TERMINAL_RUN_MISSING_OUTBOX, run_id)
            )
        if expected_outbox and len(matching_outbox) > 1:
            findings.append(
                _finding(FindingKind.DUPLICATE_TERMINAL_OUTBOX, run_id)
            )

        matching_events = [row for row in run_events if row.status == run.status]
        if run.status in _RUN_TERMINAL and not matching_events:
            findings.append(
                _finding(FindingKind.TERMINAL_RUN_MISSING_EVENT, run_id)
            )
        if run.status in _RUN_TERMINAL and len(matching_events) > 1:
            findings.append(
                _finding(FindingKind.DUPLICATE_TERMINAL_EVENT, run_id)
            )

    unique = {(item.kind, item.run_id): item for item in findings}
    return tuple(
        sorted(unique.values(), key=lambda item: (item.run_id, item.kind.value))
    )


def finding_counts(findings: tuple[Finding, ...]) -> dict[str, int]:
    return dict(sorted(Counter(item.kind.value for item in findings).items()))


def _finding(kind: FindingKind, run_id: str) -> Finding:
    return Finding(
        kind=kind,
        run_id=run_id,
        repair_key=f"repair:{kind.value}:{run_id}",
        detail=f"{kind.value} detected for {run_id}",
    )
