# Module 10 — Incident Command, Reconciliation, and Readiness

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Central question:** How do responders command an incident, reconcile durable state, repair safely, and decide whether a release is operationally ready?

## Where this module fits

Module 09 produced **Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects**. This final module consolidates the course by asking: **How do responders command an incident, reconcile durable state, repair safely, and decide whether a release is operationally ready?**

The capstone must now deliver **Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates** while preserving every earlier module result. Successful completion establishes the outgoing boundary for the next course or final program defense: **Reliability Profile 1.0, migration 008, critical journeys, deadline and resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.**

## Learning outcomes

- Assign incident command, operations, communication, and recording roles.
- Construct a timeline with source and confidence.
- Reconcile database, jobs, artifacts, and outbox state.
- Generate stable repair actions before mutation.
- Close only after user outcomes, cleanup, and regressions are verified.

## Capstone increment

Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates.

## Core reliability model

### Driving question

> How do operators coordinate under uncertainty, restore safe service, reconcile durable state, and decide whether a release is operationally ready?

Incident response separates command, diagnosis, mitigation, repair, communication, and evidence. Recovery is incomplete until durable invariants are reconciled, repairs are idempotent and journaled, and the release can demonstrate its required observability and rollback boundaries.

### 1. Incident command

One incident lead owns priorities, scope, decisions, and handoffs. Specialists investigate and execute without competing command channels.

**Failure if confused.** Five engineers independently changing retries can worsen amplification and destroy evidence.
### 2. Severity

Severity reflects user impact, data/correctness risk, duration, and urgency. It can change as evidence improves.

**Failure if confused.** A telemetry outage may be low severity until it hides a concurrent correctness failure.
### 3. Mitigation

Mitigation reduces current impact—drain, disable, throttle, fail over, or stop a worker—without claiming the defect is fixed.

**Failure if confused.** Restarting workers may restore throughput while the lease bug remains.
### 4. Repair

Repair corrects code/configuration or durable inconsistent state. It is reviewed, idempotent where possible, journaled, and bounded.

**Failure if confused.** Manually updating run rows without events/outbox creates a second inconsistency.
### 5. Reconciliation

A read-only pass compares cross-table and external invariants and emits stable findings and repair keys.

**Failure if confused.** A “fix as you scan” tool makes evidence and rollback impossible.
### 6. Timeline

A timeline records observations, decisions, actions, and outcomes with source and uncertainty. It distinguishes event time from discovery time.

**Failure if confused.** A narrative reconstructed from memory after the incident hides wrong turns.
### 7. Operational readiness

A release is ready when required journeys, controls, probes, telemetry, alerts, runbooks, migrations, rollback, and evidence boundaries are present and tested.

**Failure if confused.** Passing unit tests while removing a critical SLI is not operational readiness.
### 8. Post-incident learning

The review examines system and decision conditions, not individual blame, and maps actions to proof.

**Failure if confused.** “Operator error” is not a root-cause analysis.

For a new Analysis Runs failure:

Apply **Incident command, Severity, Mitigation** to this module’s capstone increment: Execute a full non-security incident, produce a defensible timeline, run read-only reconciliation, plan idempotent repairs, validate runbooks and alerts, and generate the Course 4 handoff to performance engineering. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Assign one incident lead | Roles, severity, decision log, and communication cadence are explicit. | No incident lead: Conflicting actions and priorities | `incident scenario proof` |
| 2 | Separate observation from inference | Timeline entries identify source, confidence, and hypothesis. | Inference logged as fact: Wrong diagnosis becomes history | `timeline schema check` |
| 3 | Mitigate before broad repair | First actions reduce impact without destroying evidence or causing more risk. | Destructive first action: Evidence and recovery options vanish | `runbook transcript` |
| 4 | Reconcile read-only first | Detection and proposed repair are separate phases. | Mutating reconciler: Detection changes system mid-scan | `reconciliation tests` |
| 5 | Use stable repair keys | Repeated plans and execution are idempotent and journaled. | Unstable repair identity: Repeated execution duplicates effects | `repair-key vectors` |
| 6 | Protect terminal invariants | Run, job, event, artifact, checksum, and outbox must agree after repair. | Partial terminal repair: Tables disagree after fix | `terminal reconciliation` |
| 7 | Validate operational release requirements | Required SLI, alert, runbook, probe, migration, and rollback evidence are release gates. | Release loses observability: Failure cannot be detected | `release proof` |
| 8 | Turn actions into proof | Every material remediation maps to a regression, requirement, owner, and completion evidence. | Actions without verification: Postmortem produces backlog only | `post-incident action map` |


### Evidence boundary

Scripted incidents prove role, timeline, reconciliation, and release gates; they do not prove a team can execute those practices under a real incident.

## Worked failures

### Case 1 — Everyone is incident commander

#### Initial system

API, database, and worker owners independently restart, change retry counts, and delete jobs. Evidence becomes inconsistent and impact grows.


#### Correct design

Assign one lead, one operations executor, focused investigators, and one recorder. Changes are proposed, approved, timestamped, and reversible.


#### Lesson

Coordination is a reliability mechanism.
### Case 2 — Reconciler repairs while scanning

#### Initial system

The tool finds a completed run without outbox and immediately inserts one, then later discovers the artifact checksum is wrong. A false completion webhook may be sent.


#### Correct design

Phase 1 emits immutable findings and stable repair keys. A reviewed plan orders safe repairs; execution journals before/after evidence and reruns detection.


#### Lesson

Detection must not mutate the evidence it evaluates.
### Case 3 — Restart declared resolution

#### Initial system

Restarting workers drains backlog, so the incident is closed despite recurring lease expiry.


#### Correct design

Call restart a mitigation, monitor recurrence, repair the lease defect, add regression and alert, then close after verification.


#### Lesson

Restored service is not always repaired service.
### Case 4 — Compatible but unobservable release

#### Initial system

API and migration compatibility pass, but the new release removes run-start freshness and makes collector connectivity part of liveness.


#### Correct design

Reliability release proof rejects loss of required SLI and diagnostic dependency coupling.


#### Lesson

Operational compatibility extends beyond schema compatibility.

## Python implementation

### Mechanism under review

Generate immutable findings and stable repair keys, validate runbooks, and produce a release-readiness report without combining scan and mutation.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py`
- `capstone/tracks/python-fastapi/src/api_reliability/runbooks.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_telemetry_reconcile.py`

### Executable invariant

```python
from api_reliability.reconcile import RunRow, Snapshot, inspect

findings = inspect(Snapshot(
    runs=(RunRow("run-1", "completed"),), jobs=(), artifacts=(), outbox=(), events=(),
))
assert {item.kind.value for item in findings} == {
    "completed-run-missing-artifact",
    "terminal-run-missing-event",
    "terminal-run-missing-outbox",
}
```

The cited files must expose the complete **Incident Command, Reconciliation, and Readiness** implementation path and its negative regression evidence.

### Guided failure investigation — Everyone is incident commander

**Initial condition.** API, database, and worker owners independently restart, change retry counts, and delete jobs. Evidence becomes inconsistent and impact grows.

**Expected repair.** Assign one lead, one operations executor, focused investigators, and one recorder. Changes are proposed, approved, timestamped, and reversible.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=10 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **No incident lead.** Conflicting actions and priorities The decisive check is role/timeline audit.
- **Inference logged as fact.** Wrong diagnosis becomes history The decisive check is source/confidence schema.
- **Destructive first action.** Evidence and recovery options vanish The decisive check is runbook stop check.
- **Mutating reconciler.** Detection changes system mid-scan The decisive check is read-only transaction proof.
- **Unstable repair identity.** Repeated execution duplicates effects The decisive check is repair-key idempotency.
- **Partial terminal repair.** Tables disagree after fix The decisive check is cross-invariant scan.

## TypeScript implementation

### Mechanism under review

Model findings and repair plans as discriminated immutable records, preserve bigint-safe identities, and prove repeated planning produces identical keys.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

### Executable invariant

```typescript
const findings = inspect({
  runs: [{ runId: "run-1", status: "completed" }],
  jobs: [], artifacts: [], outbox: [], events: [],
});
if (findings.length !== 3) throw new Error("incomplete reconciliation");
```

The cited files must expose the complete **Incident Command, Reconciliation, and Readiness** implementation path and its negative regression evidence.

### Guided failure investigation — Everyone is incident commander

**Initial condition.** API, database, and worker owners independently restart, change retry counts, and delete jobs. Evidence becomes inconsistent and impact grows.

**Expected repair.** Assign one lead, one operations executor, focused investigators, and one recorder. Changes are proposed, approved, timestamped, and reversible.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=10 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **No incident lead.** Conflicting actions and priorities The decisive check is role/timeline audit.
- **Inference logged as fact.** Wrong diagnosis becomes history The decisive check is source/confidence schema.
- **Destructive first action.** Evidence and recovery options vanish The decisive check is runbook stop check.
- **Mutating reconciler.** Detection changes system mid-scan The decisive check is read-only transaction proof.
- **Unstable repair identity.** Repeated execution duplicates effects The decisive check is repair-key idempotency.
- **Partial terminal repair.** Tables disagree after fix The decisive check is cross-invariant scan.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **No incident lead** | Everyone begins debugging immediately. | Decisions conflict and containment lacks ownership. | A small simulation has cooperative participants. | role/timeline audit. |
| **Inference logged as fact** | A plausible hypothesis is written quickly. | Later responders cannot distinguish observation from interpretation. | The initial hypothesis happens to be correct in the fixture. | source/confidence schema. |
| **Destructive first action** | Deleting or restarting appears to clear symptoms. | Evidence is lost and durable inconsistency can worsen. | The toy state is disposable. | runbook stop check. |
| **Mutating reconciler** | Automatic repair seems efficient. | Diagnosis and mutation become inseparable and unsafe to rerun. | The fixture contains only one obvious repair. | read-only transaction proof. |
| **Unstable repair identity** | Each repair run generates a new request ID. | Repeated repair can apply the same effect more than once. | The test performs one repair. | repair-key idempotency. |
| **Partial terminal repair** | Updating the visible run state appears sufficient. | Jobs, events, artifacts, or outbox records remain inconsistent. | The API response reads only one table. | cross-invariant scan. |
| **Release loses observability** | The code change is behaviorally compatible. | Operators cannot distinguish or diagnose the new version. | Contract and unit tests do not inspect telemetry. | profile gate. |
| **Actions without verification** | A command completed without error. | Containment or repair is assumed rather than established. | The test asserts exit status, not postcondition. | action-proof map. |

## What you add to the capstone

### Increment

Execute a full non-security incident, produce a defensible timeline, run read-only reconciliation, plan idempotent repairs, validate runbooks and alerts, and generate the Course 4 handoff to performance engineering.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py`
- `capstone/tracks/python-fastapi/src/api_reliability/runbooks.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_telemetry_reconcile.py`
- `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Assign one incident lead.** Roles, severity, decision log, and communication cadence are explicit.
- **Separate observation from inference.** Timeline entries identify source, confidence, and hypothesis.
- **Mitigate before broad repair.** First actions reduce impact without destroying evidence or causing more risk.
- **Reconcile read-only first.** Detection and proposed repair are separate phases.
- The planted failure **Everyone is incident commander** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Everyone is incident commander**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Assign one lead, one operations executor, focused investigators, and one recorder. Changes are proposed, approved, timestamped, and reversible.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How do operators coordinate under uncertainty, restore safe service, reconcile durable state, and decide whether a release is operationally ready?” is decided by durable state rather than telemetry?
2. What is the smallest fault that disproves the design?
3. Which label, context value, or event field could become unbounded?
4. What happens after restart halfway through the operation?
5. Which Course 3 security constraint could observability violate?
6. Which proof is local and which needs a live environment?
7. How do the two tracks preserve the same invariant idiomatically?
8. What behavior would block release despite OpenAPI compatibility?

### Required artifacts

Record `accept`, `accept-with-residual-risk`, or `reject`. A rejection names the failed requirement and exact evidence needed for reconsideration.

## Representative implementation

These are the smallest useful entry points for **Incident Command, Reconciliation, and Readiness**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py`

```python
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
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`

```text
// Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
export type FindingKind =
  | "run-without-job"
  | "job-without-run"
  | "terminal-job-nonterminal-run"
  | "terminal-run-nonterminal-job"
  | "completed-run-missing-artifact"
  | "multiple-artifacts"
  | "artifact-without-completed-run"
  | "terminal-run-missing-outbox"
  | "duplicate-terminal-outbox"
  | "terminal-run-missing-event"
  | "duplicate-terminal-event";

export interface Snapshot {
  readonly runs: readonly { readonly runId: string; readonly status: string }[];
  readonly jobs: readonly { readonly runId: string; readonly status: string }[];
  readonly artifacts: readonly { readonly runId: string; readonly artifactId: string }[];
  readonly outbox: readonly { readonly runId: string; readonly eventType: string }[];
  readonly events?: readonly { readonly runId: string; readonly status: string }[];
}

export interface Finding {
  readonly kind: FindingKind;
  readonly runId: string;
  readonly repairKey: string;
  readonly detail: string;
}

const RUN_TERMINAL = new Set(["completed", "failed", "canceled"]);
const JOB_TERMINAL = new Set(["completed", "dead", "canceled"]);
const OUTBOX_EXPECTED: Readonly<Record<string, string>> = {
  completed: "analysis.completed",
  failed: "analysis.failed",
};

function append<K, V>(map: Map<K, V[]>, key: K, value: V): void {
  const values = map.get(key) ?? [];
  values.push(value);
  map.set(key, values);
}

export function inspect(snapshot: Snapshot): Finding[] {
  const runs = new Map(snapshot.runs.map((row) => [row.runId, row]));
  const jobs = new Map(snapshot.jobs.map((row) => [row.runId, row]));
  const artifacts = new Map<string, (typeof snapshot.artifacts)[number][]>();
  const outbox = new Map<string, (typeof snapshot.outbox)[number][]>();
  const events = new Map<string, NonNullable<Snapshot["events"]>[number][]>();
  for (const row of snapshot.artifacts) append(artifacts, row.runId, row);
  for (const row of snapshot.outbox) append(outbox, row.runId, row);
  for (const row of snapshot.events ?? []) append(events, row.runId, row);

  const identifiers = new Set([
    ...runs.keys(), ...jobs.keys(), ...artifacts.keys(), ...outbox.keys(), ...events.keys(),
  ]);
  const findings: Finding[] = [];
  for (const runId of [...identifiers].sort()) {
    const run = runs.get(runId);
    const job = jobs.get(runId);
    const runArtifacts = artifacts.get(runId) ?? [];
    const runOutbox = outbox.get(runId) ?? [];
    const runEvents = events.get(runId) ?? [];

    if (run === undefined && job !== undefined) {
      findings.push(finding("job-without-run", runId));
      continue;
```

Compare the two tracks by this invariant: **operators diagnose from telemetry but reconcile and repair from read-only durable facts using stable, idempotent repair identifiers**. The intended implementation difference is: data-access mechanics differ; findings and repair plans must be deterministic and reviewable.

## Course exit

The ten module results now satisfy this course promise: A reliability profile with deadlines, resilience, lifecycle control, telemetry, SLIs, SLOs, alerting, fault injection, reconciliation, and incident readiness. The next course is **API Performance, Capacity, and Traffic Engineering**; it consumes the outgoing handoff rather than reinterpreting completed work.

## Module synthesis

You are ready to leave this module when you can **Assign incident command, operations, communication, and recording roles, Construct a timeline with source and confidence, and Reconcile database, jobs, artifacts, and outbox state** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove or bypass the central control for Incident Command, Reconciliation, and Readiness in a temporary branch** and requiring the following oracle: **Decision log has one command owner and source-linked entries; Mitigation reduces impact without duplicate terminal effects; Initial reconciliation performs no mutation; Repeated repair execution is idempotent.**

The cumulative platform now includes **Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Complete the course final defense and outgoing handoff described in [Capstone](../capstone.md). Course 5 may treat only the manifested handoff as settled.
