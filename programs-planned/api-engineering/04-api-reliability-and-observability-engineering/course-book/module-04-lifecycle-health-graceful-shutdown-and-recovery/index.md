# Module 04 — Lifecycle, Health, Shutdown, and Recovery

> **Program stage:** Course 4 of 6 — Operate and recover the promise.

> **Central question:** How do APIs, workers, and dispatchers start, become ready, drain, stop, and recover without losing accepted work?

## Where this module fits

Implement explicit lifecycle states, meaningful health decisions, bounded drain, and lease-aware worker shutdown. You arrive from Module 03 with all earlier checkpoints still green. API 1.2 and security profile 1.0 are fixed. This course adds budgets, telemetry, recovery, and operational decisions; observations may explain durable truth but never replace it. The result is the baseline for **Telemetry Architecture and Structured Events**.

## Learning outcomes

- Separate startup, liveness, and readiness.
- Stop accepting before draining.
- Bound graceful shutdown and preserve durable claims.
- Recover incomplete work on startup.
- Make health endpoints report service ability, not every dependency detail.

## Capstone result

Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation.

API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.

## Core reliability model

### Driving question

> How does an API, worker, and dispatcher start, accept work, drain, stop, and recover without lying to traffic routers or abandoning durable effects?

Lifecycle is an explicit state machine. Liveness says the process can make local progress, readiness says this instance may receive new work, and draining prevents new admission while preserving owned work and durable recovery evidence.

### 1. Lifecycle state machine

The process moves through created, starting, ready, draining, stopped, and failed states under explicit transitions. Health endpoints expose state; they do not invent it.

**Failure if confused.** A Boolean healthy flag cannot distinguish slow startup from deadlock or intentional drain.
### 2. Startup gate

Startup verifies configuration, migration compatibility, secret availability, and required local resources before readiness. It may tolerate recoverable optional telemetry dependencies.

**Failure if confused.** Serving requests before migrations are compatible can create durable corruption even when the process responds.
### 3. Liveness

Liveness asks whether this process should be restarted because it cannot make local forward progress. It must not depend on every remote dependency.

**Failure if confused.** Making liveness fail when the telemetry collector is down creates restart storms without repairing telemetry.
### 4. Readiness

Readiness is an admission decision for this instance and journey. Required dependency exhaustion, migration mismatch, or drain may make it unready while the process remains live.

**Failure if confused.** A live but drained API must not receive new requests.
### 5. Drain

Drain first removes new admission, then waits for bounded in-flight work, transfers or releases leases, flushes bounded evidence, and stops.

**Failure if confused.** Stopping listeners after killing workers can strand jobs or return partial responses.
### 6. Owned work

A process may own requests, database transactions, worker leases, temporary files, or export batches. Each ownership type has a release, handoff, or recovery rule.

**Failure if confused.** A worker cannot simply exit while holding a lease and assume another worker will immediately recover it.
### 7. Recovery

Restart recovery derives from durable state and lease rules, not process memory. Recovery is measured and reconciled.

**Failure if confused.** An in-memory retry queue disappears on restart despite perfect readiness before shutdown.
### 8. Probe hysteresis

Thresholds, startup grace, and recovery conditions prevent brief transients from flapping readiness or triggering repeated restarts.

**Failure if confused.** One failed database ping should not necessarily churn all replicas.

For a new Analysis Runs failure:

Apply **Lifecycle state machine, Startup gate, Liveness** to this module’s capstone increment: Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Model lifecycle explicitly | Every process type has named states and allowed transitions with timestamps and reasons. | Collapsed health endpoint: Routers and restart controllers receive the same signal | `lifecycle transition tests` |
| 2 | Keep liveness local | Remote dependency failure cannot by itself make liveness fail. | Remote liveness dependency: Dependency outage causes restart storm | `collector and database outage vectors` |
| 3 | Make readiness journey-aware | Readiness reflects whether this instance can safely accept its required work. | Admission during drain: Requests terminate mid-flight | `health vectors` |
| 4 | Drain before termination | Admission closes before in-flight work is awaited or transferred. | Unbounded shutdown: Deployment never finishes | `drain-order test` |
| 5 | Bound shutdown | Every shutdown phase has a deadline and a documented fallback. | Lease abandoned silently: Jobs wait for full expiry or duplicate | `shutdown budget test` |
| 6 | Release or fence leases | Workers renew, release, or allow leases to expire without permitting stale completion. | Memory-only recovery: Restart loses queued work | `worker termination scenario` |
| 7 | Recover from durable state | Restart behavior is derived from committed rows, immutable objects, and repair journal—not memory. | Readiness flapping: Instances churn under transient failure | `restart reconciliation test` |
| 8 | Do not make telemetry authoritative | Exporter flush failure is reported but cannot change durable business outcome. | Telemetry flush blocks stop: Diagnostic path consumes shutdown budget | `collector outage shutdown test` |


### Evidence boundary

Lifecycle tests prove state transitions; orchestrator signal ordering, load-balancer removal, and real process drain timing require live execution.

## Worked failures


### Case 1 — Collector-dependent liveness

#### Initial system

The service marks liveness false whenever the OpenTelemetry collector is unreachable. Orchestration restarts every instance, increasing load while customer operations were otherwise healthy.


#### Correct design

Keep liveness local. Record exporter failure and bounded drops; readiness remains based on required service dependencies and safe admission.


#### Lesson

A diagnostic dependency must not become a restart oracle.
### Case 2 — Drain after termination signal

#### Initial system

The API continues accepting requests while the termination grace period is consumed flushing telemetry. New work is killed when the deadline expires.


#### Correct design

Transition to draining immediately, make readiness false, stop new admission, complete bounded in-flight work, then flush telemetry only inside a smaller remaining budget.


#### Lesson

Shutdown order is a correctness property.
### Case 3 — Worker killed after artifact write

#### Initial system

A worker writes immutable artifact bytes, receives termination, and exits before committing the terminal transaction. Another worker retries.


#### Correct design

Content-addressed no-clobber storage makes publication repeatable. Durable job lease and stale-worker fencing decide who may commit completion. Reconciliation detects orphaned immutable content.


#### Lesson

Recovery requires idempotent external effects plus durable authority.
### Case 4 — Migration mismatch hidden by readiness

#### Initial system

A new binary expects migration 008, but readiness checks only database connectivity. It accepts work and fails later inside reconciliation.


#### Correct design

Startup reads the migration revision and fails readiness with a specific incompatibility reason while liveness remains true long enough for diagnosis.


#### Lesson

Connectivity is not compatibility.

## Python implementation

### Mechanism under review

Drive the lifecycle evaluator with a manual clock, add ASGI readiness/drain behavior, and prove telemetry flush cannot extend the correctness budget.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/health.py`
- `capstone/tracks/python-fastapi/src/api_reliability/fastapi_adapter.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_metrics_health.py`

### Executable invariant

```python
from api_reliability.health import (
    ComponentHealth, HealthEvaluator, LifecyclePhase
)

snapshot = HealthEvaluator().evaluate(
    phase=LifecyclePhase.DRAINING,
    startup_complete=True,
    event_loop_progressing=True,
    components=[ComponentHealth("postgres", True, True)],
)
assert snapshot.live is True
assert snapshot.ready is False
```

The cited files own the complete implementation and regression evidence.

### Guided failure investigation — Collector-dependent liveness

**Initial condition.** The service marks liveness false whenever the OpenTelemetry collector is unreachable. Orchestration restarts every instance, increasing load while customer operations were otherwise healthy.

**Expected repair.** Keep liveness local. Record exporter failure and bounded drops; readiness remains based on required service dependencies and safe admission.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=04 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Collapsed health endpoint.** Routers and restart controllers receive the same signal The decisive check is separate state and probe tests.
- **Remote liveness dependency.** Dependency outage causes restart storm The decisive check is remote-outage vector.
- **Admission during drain.** Requests terminate mid-flight The decisive check is drain-order transcript.
- **Unbounded shutdown.** Deployment never finishes The decisive check is phase deadline evidence.
- **Lease abandoned silently.** Jobs wait for full expiry or duplicate The decisive check is lease transition audit.
- **Memory-only recovery.** Restart loses queued work The decisive check is durable-state restart test.

## TypeScript implementation

### Mechanism under review

Implement equivalent Fastify hooks and shutdown ordering, using AbortSignal for bounded waits while keeping durable recovery independent of process promises.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/health.ts`
- `capstone/tracks/typescript-fastify/src/reliability/index.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/metrics-health.test.mjs`

### Executable invariant

```typescript
const snapshot = evaluateHealth({
  phase: "draining", startupComplete: true, eventLoopProgressing: true,
  components: [{ name: "postgres", requiredForReadiness: true, available: true }],
});
if (!snapshot.live || snapshot.ready) throw new Error("drain contract violated");
```

The cited files own the complete implementation and regression evidence.

### Guided failure investigation — Collector-dependent liveness

**Initial condition.** The service marks liveness false whenever the OpenTelemetry collector is unreachable. Orchestration restarts every instance, increasing load while customer operations were otherwise healthy.

**Expected repair.** Keep liveness local. Record exporter failure and bounded drops; readiness remains based on required service dependencies and safe admission.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=04 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Collapsed health endpoint.** Routers and restart controllers receive the same signal The decisive check is separate state and probe tests.
- **Remote liveness dependency.** Dependency outage causes restart storm The decisive check is remote-outage vector.
- **Admission during drain.** Requests terminate mid-flight The decisive check is drain-order transcript.
- **Unbounded shutdown.** Deployment never finishes The decisive check is phase deadline evidence.
- **Lease abandoned silently.** Jobs wait for full expiry or duplicate The decisive check is lease transition audit.
- **Memory-only recovery.** Restart loses queued work The decisive check is durable-state restart test.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Collapsed health endpoint** | One endpoint and one boolean are easy for platforms. | Liveness, readiness, and accepting traffic have different meanings. | A fully healthy process returns the same value for all three. | separate state and probe tests. |
| **Remote liveness dependency** | Checking every dependency appears thorough. | A healthy process is restarted because a remote service is unavailable. | Normal tests keep dependencies available. | remote-outage vector. |
| **Admission during drain** | The listener remains open while existing work finishes. | New work enters after shutdown has begun and may be abandoned. | Shutdown tests often contain only pre-existing requests. | drain-order transcript. |
| **Unbounded shutdown** | Waiting forever seems safer than interruption. | Deployment and recovery stall indefinitely. | Short jobs complete before the hidden bound matters. | phase deadline evidence. |
| **Lease abandoned silently** | Process exit appears to transfer responsibility automatically. | Work remains invisible until lease expiry and no operator evidence explains the delay. | Graceful test shutdown releases every lease. | lease transition audit. |
| **Memory-only recovery** | In-process state is convenient for startup. | Restart loses the information needed to resume or reconcile accepted work. | Tests do not kill the process between acceptance and completion. | durable-state restart test. |
| **Readiness flapping** | Every probe reflects instantaneous dependency state. | Transient noise repeatedly adds and removes capacity. | Steady-state tests do not vary the dependency near the threshold. | hysteresis sequence. |
| **Telemetry flush blocks stop** | Flushing every pending event appears lossless. | Shutdown exceeds its deadline because the exporter is unavailable. | The test exporter drains immediately. | bounded flush assertion. |

## What you add to the capstone

### Increment

Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/health.py`
- `capstone/tracks/python-fastapi/src/api_reliability/fastapi_adapter.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_metrics_health.py`
- `capstone/tracks/typescript-fastify/src/reliability/health.ts`
- `capstone/tracks/typescript-fastify/src/reliability/index.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/metrics-health.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Model lifecycle explicitly.** Every process type has named states and allowed transitions with timestamps and reasons.
- **Keep liveness local.** Remote dependency failure cannot by itself make liveness fail.
- **Make readiness journey-aware.** Readiness reflects whether this instance can safely accept its required work.
- **Drain before termination.** Admission closes before in-flight work is awaited or transferred.
- The planted failure **Collector-dependent liveness** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Collector-dependent liveness**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Keep liveness local. Record exporter failure and bounded drops; readiness remains based on required service dependencies and safe admission.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How does an API, worker, and dispatcher start, accept work, drain, stop, and recover without lying to traffic routers or abandoning durable effects?” is decided by durable state rather than telemetry?
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

These are the smallest useful entry points for **Lifecycle, Health, Shutdown, and Recovery**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/health.py`

```python
from enum import Enum


class LifecyclePhase(str, Enum):
    STARTING = "starting"
    ACCEPTING = "accepting"
    DRAINING = "draining"
    STOPPED = "stopped"
    FAILED = "failed"


_ALLOWED_TRANSITIONS: dict[LifecyclePhase, frozenset[LifecyclePhase]] = {
    LifecyclePhase.STARTING: frozenset(
        {LifecyclePhase.ACCEPTING, LifecyclePhase.DRAINING, LifecyclePhase.FAILED}
    ),
    LifecyclePhase.ACCEPTING: frozenset(
        {LifecyclePhase.DRAINING, LifecyclePhase.FAILED}
    ),
    LifecyclePhase.DRAINING: frozenset(
        {LifecyclePhase.STOPPED, LifecyclePhase.FAILED}
    ),
    LifecyclePhase.FAILED: frozenset({LifecyclePhase.STOPPED}),
    LifecyclePhase.STOPPED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class LifecycleTransition:
    from_phase: LifecyclePhase
    to_phase: LifecyclePhase
    reason: str
    timestamp_ms: int


@dataclass(slots=True)
class LifecycleController:
    phase: LifecyclePhase = LifecyclePhase.STARTING
    history: list[LifecycleTransition] = field(default_factory=list)

    def transition(
        self,
        to_phase: LifecyclePhase,
        *,
        reason: str,
        timestamp_ms: int,
    ) -> LifecycleTransition:
        if not reason or len(reason) > 120:
            raise ValueError("transition reason must contain 1..120 characters")
        if to_phase not in _ALLOWED_TRANSITIONS[self.phase]:
            raise ValueError(
                f"invalid lifecycle transition {self.phase.value}->{to_phase.value}"
            )
        item = LifecycleTransition(self.phase, to_phase, reason, timestamp_ms)
        self.phase = to_phase
        self.history.append(item)
        return item


@dataclass(frozen=True, slots=True)
class ComponentHealth:
    name: str
    required_for_readiness: bool
    available: bool
    detail: str = ""
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/health.ts`

```typescript
export type LifecyclePhase =
  | "starting"
  | "accepting"
  | "draining"
  | "stopped"
  | "failed";

export interface LifecycleTransition {
  readonly fromPhase: LifecyclePhase;
  readonly toPhase: LifecyclePhase;
  readonly reason: string;
  readonly timestampMs: number;
}

const ALLOWED: Readonly<Record<LifecyclePhase, readonly LifecyclePhase[]>> = {
  starting: ["accepting", "draining", "failed"],
  accepting: ["draining", "failed"],
  draining: ["stopped", "failed"],
  failed: ["stopped"],
  stopped: [],
};

export class LifecycleController {
  public readonly history: LifecycleTransition[] = [];
  public constructor(public phase: LifecyclePhase = "starting") {}
  public transition(
    toPhase: LifecyclePhase,
    input: { reason: string; timestampMs: number },
  ): LifecycleTransition {
    if (input.reason.length < 1 || input.reason.length > 120) {
      throw new Error("transition reason must contain 1..120 characters");
    }
    if (!ALLOWED[this.phase].includes(toPhase)) {
      throw new Error(`invalid lifecycle transition ${this.phase}->${toPhase}`);
    }
    const item = {
      fromPhase: this.phase,
      toPhase,
      reason: input.reason,
      timestampMs: input.timestampMs,
    } as const;
    this.phase = toPhase;
    this.history.push(item);
    return item;
  }
}

export interface ComponentHealth {
  readonly name: string;
  readonly requiredForReadiness: boolean;
  readonly available: boolean;
  readonly detail?: string;
}
export interface HealthSnapshot {
  readonly live: boolean;
  readonly ready: boolean;
  readonly startupComplete: boolean;
  readonly phase: LifecyclePhase;
  readonly reasons: readonly string[];
}

export function evaluateHealth(input: {
  phase: LifecyclePhase;
  startupComplete: boolean;
  eventLoopProgressing: boolean;
```

Compare the two tracks by this invariant: **liveness reports process existence, readiness reports safe admission, and draining stops new work before owned work is released**. The intended implementation difference is: framework shutdown hooks differ; lifecycle states and observable probe results must match.

## Module synthesis

The module answer to “How does a process start, accept work, drain, stop, and recover without lying to orchestrators or losing durable work?” is now executable in the capstone: API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.

## Next in the story

Module 05, [Telemetry Architecture and Structured Events](../module-05-telemetry-architecture-and-structured-operational-events/index.md), asks: *What should the system record so an operator can reconstruct behavior without leaking secrets or blocking the request path?* The current checkpoint must remain green while that new responsibility is added.
