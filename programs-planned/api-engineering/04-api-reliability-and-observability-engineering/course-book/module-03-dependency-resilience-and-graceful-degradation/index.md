# Module 03 — Dependency Resilience and Graceful Degradation

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Central question:** How should circuits, bulkheads, and degradation be scoped so they contain rather than hide dependency failure?

## Where this module fits

Module 02 produced **Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation**. This module extends that result by asking: **How should circuits, bulkheads, and degradation be scoped so they contain rather than hide dependency failure?**

The new capstone increment is **Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses**. It becomes the prerequisite for **Lifecycle, Health, Shutdown, and Recovery**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Classify dependency failures and ownership.
- Use bulkheads to bound local resource consumption.
- Design circuit state and half-open probe ownership.
- Avoid fallbacks that fabricate correctness.
- Keep telemetry failure from becoming business failure.

## Capstone increment

Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses.

## Core reliability model

### Driving question

> How does the service contain dependency failure without amplifying it, lying about success, or collapsing unrelated journeys?

Resilience mechanisms are dependency-specific controls with explicit state, scope, and failure semantics—not decorations applied to every call.

### 1. Dependency contract

A dependency policy states operation, deadline, retry owner, concurrency budget, circuit scope, fallback, and durable-effect boundary.

**Failure if confused.** PostgreSQL transactions and telemetry export require different failure treatment.
### 2. Circuit breaker

A circuit rejects calls after classified failures, then permits bounded probes after an open interval. It protects capacity; it does not repair the dependency.

**Failure if confused.** Opening the artifact circuit cannot declare an artifact published.
### 3. Bulkhead

A bulkhead reserves finite concurrent capacity so one slow dependency cannot consume every worker or connection.

**Failure if confused.** Webhook dispatch must not occupy permits required for API database work.
### 4. Graceful degradation

A degraded path preserves the contract and tells the truth. Partial or stale data is valid only when the operation defines it.

**Failure if confused.** Diagnostics may omit optional telemetry detail; run status cannot be guessed from traces.
### 5. Fallback

A fallback is a named alternative source or behavior with known freshness and consistency. Catching an exception and returning success is not a fallback.

**Failure if confused.** Serving immutable content from a validated cache can be valid; inventing analysis success is not.
### 6. Failure isolation

Isolation limits blast radius across journeys, tenants, or resource pools. Hidden shared resources can defeat apparent separation.

**Failure if confused.** Separate semaphores do not isolate if both paths exhaust one database pool.
### 7. Recovery probe

Half-open probes are bounded, representative, and preferably side-effect free. User traffic is not an uncontrolled experiment.

**Failure if confused.** A storage metadata read is safer than publishing an artifact as a probe.

For a new Analysis Runs failure:

Apply **Dependency contract, Circuit breaker, Bulkhead** to this module’s capstone increment: Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Name every protected dependency | No global generic circuit hides distinct failure domains. | Global circuit: Unrelated operations fail together | `dependency policy validation` |
| 2 | Count classified failures | Only relevant dependency failures affect circuit state. | False-success fallback: Durable state contradicts response | `failure-class tests` |
| 3 | Measure bulkhead capacity | Permit counts derive from resource budgets and expose saturation with bounded labels. | Unbounded half-open probes: Recovery spike overloads dependency | `bulkhead tests` |
| 4 | Preserve truth in fallback | No degraded path reports durable success without the effect. | Bulkhead over shared bottleneck: Apparent isolation fails | `false-success test` |
| 5 | Keep telemetry fail-open | Exporter failure records drops but does not fail customer work. | Circuit on client errors: Healthy dependency appears failed | `collector-outage test` |
| 6 | Keep required durability fail-closed | Mutations cannot be acknowledged while required transaction state is unavailable. | Telemetry fail-closed: Collector outage becomes API outage | `database fault scenario` |
| 7 | Bound half-open probes | Only configured probes execute; other calls fail fast. | Permanent error retried: Backlog grows indefinitely | `circuit state tests` |
| 8 | Observe recovery transitions | Circuit and bulkhead transitions use bounded metrics/events. | No transition signal: Local circuit is invisible | `transition assertions` |


### Evidence boundary

State-machine tests prove classification and isolation logic; real dependency recovery and shared-resource contention require an integration environment.

## Worked failures

### Case 1 — Telemetry collector outage

#### Initial system

The OTLP exporter blocks request completion and returns 500 when the collector is unreachable.


#### Correct design

Use bounded asynchronous export and local drop accounting. Customer requests complete from authoritative state.


#### Lesson

Observability must not become a new availability dependency.
### Case 2 — Artifact storage failure

#### Initial system

The worker marks a run completed and schedules upload later after storage failure.


#### Correct design

Keep the run non-completed or fail it according to policy; no terminal completed event exists without artifact evidence.


#### Lesson

Graceful degradation cannot violate terminal invariants.
### Case 3 — Webhook receiver storm

#### Initial system

One slow receiver consumes all dispatch tasks and delays every tenant.


#### Correct design

Use bounded/fair concurrency, deadlines, durable retry schedule, and backlog visibility while API capacity remains isolated.


#### Lesson

A bulkhead also needs fairness and durable queue evidence.
### Case 4 — Over-broad circuit

#### Initial system

One failed diagnostics query opens a global database circuit and rejects run submissions.


#### Correct design

Scope circuit state to dependency operation/failure domain; classify pool/global failure separately.


#### Lesson

A circuit that is too broad increases blast radius.

## Python implementation

### Mechanism under review

Drive circuit transitions with ManualClock and verify exception-safe bulkhead permit release.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/circuit.py`
- `capstone/tracks/python-fastapi/src/api_reliability/bulkhead.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_retry_circuit.py`

### Executable invariant

```python
from api_reliability.circuit import CircuitBreaker, CircuitOpen
from api_reliability.clock import ManualClock

clock = ManualClock(0)
breaker = CircuitBreaker(failure_threshold=2, open_duration_ms=500)
breaker.allow(clock); breaker.failure(clock)
breaker.allow(clock); breaker.failure(clock)
try:
    breaker.allow(clock)
except CircuitOpen:
    pass
else:
    raise AssertionError("open circuit admitted a call")
```

The cited files must expose the complete **Dependency Resilience and Graceful Degradation** implementation path and its negative regression evidence.

### Guided failure investigation — Telemetry collector outage

**Initial condition.** The OTLP exporter blocks request completion and returns 500 when the collector is unreachable.

**Expected repair.** Use bounded asynchronous export and local drop accounting. Customer requests complete from authoritative state.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=03 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Global circuit.** Unrelated operations fail together The decisive check is operation-scoped state.
- **False-success fallback.** Durable state contradicts response The decisive check is terminal reconciliation.
- **Unbounded half-open probes.** Recovery spike overloads dependency The decisive check is probe concurrency test.
- **Bulkhead over shared bottleneck.** Apparent isolation fails The decisive check is pool saturation experiment.
- **Circuit on client errors.** Healthy dependency appears failed The decisive check is classification vectors.
- **Telemetry fail-closed.** Collector outage becomes API outage The decisive check is collector fault experiment.

## TypeScript implementation

### Mechanism under review

Model explicit state transitions and async permit release without relying on SDK-specific resilience packages.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/circuit.ts`
- `capstone/tracks/typescript-fastify/src/reliability/bulkhead.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/retry-circuit.test.mjs`

### Executable invariant

```typescript
const clock = new ManualClock(0);
const breaker = new CircuitBreaker(2, 500);
breaker.allow(clock); breaker.failure(clock);
breaker.allow(clock); breaker.failure(clock);
if (breaker.state !== "open") throw new Error("circuit did not open");
```

The cited files must expose the complete **Dependency Resilience and Graceful Degradation** implementation path and its negative regression evidence.

### Guided failure investigation — Telemetry collector outage

**Initial condition.** The OTLP exporter blocks request completion and returns 500 when the collector is unreachable.

**Expected repair.** Use bounded asynchronous export and local drop accounting. Customer requests complete from authoritative state.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=03 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Global circuit.** Unrelated operations fail together The decisive check is operation-scoped state.
- **False-success fallback.** Durable state contradicts response The decisive check is terminal reconciliation.
- **Unbounded half-open probes.** Recovery spike overloads dependency The decisive check is probe concurrency test.
- **Bulkhead over shared bottleneck.** Apparent isolation fails The decisive check is pool saturation experiment.
- **Circuit on client errors.** Healthy dependency appears failed The decisive check is classification vectors.
- **Telemetry fail-closed.** Collector outage becomes API outage The decisive check is collector fault experiment.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Global circuit** | One switch is easier to implement and inspect. | Failure in one operation or tenant disables unrelated healthy traffic. | A single-dependency test never demonstrates isolation. | operation-scoped state. |
| **False-success fallback** | Returning cached or empty data can keep the status code green. | The API reports an outcome that is no longer true or complete. | Schema checks pass because the representation remains syntactically valid. | terminal reconciliation. |
| **Unbounded half-open probes** | Allowing all waiting requests seems to speed recovery. | A recovering dependency receives a new traffic spike. | A single probe test cannot expose concurrent ownership. | probe concurrency test. |
| **Bulkhead over shared bottleneck** | Separate application semaphores look isolated. | Both groups still exhaust the same connection pool or CPU. | Tests do not saturate the actual shared resource. | pool saturation experiment. |
| **Circuit on client errors** | All non-success statuses are counted together. | Valid 4xx traffic opens a circuit against a healthy dependency. | Happy-path tests contain no malformed or unauthorized requests. | classification vectors. |
| **Telemetry fail-closed** | Operators want every event exported. | Exporter failure blocks or fails the user operation. | The local exporter is healthy during normal tests. | collector fault experiment. |
| **Permanent error retried** | Uniform retry code is simpler. | Invalid requests or forbidden destinations consume budget repeatedly. | Only transient fixtures are used in the success suite. | retry disposition audit. |
| **No transition signal** | The current circuit state is visible in memory. | Operators cannot reconstruct when and why the service changed behavior. | A state-machine unit test does not inspect operational evidence. | state-change evidence. |

## What you add to the capstone

### Increment

Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/circuit.py`
- `capstone/tracks/python-fastapi/src/api_reliability/bulkhead.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_retry_circuit.py`
- `capstone/tracks/typescript-fastify/src/reliability/circuit.ts`
- `capstone/tracks/typescript-fastify/src/reliability/bulkhead.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/retry-circuit.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Name every protected dependency.** No global generic circuit hides distinct failure domains.
- **Count classified failures.** Only relevant dependency failures affect circuit state.
- **Measure bulkhead capacity.** Permit counts derive from resource budgets and expose saturation with bounded labels.
- **Preserve truth in fallback.** No degraded path reports durable success without the effect.
- The planted failure **Telemetry collector outage** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Telemetry collector outage**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Use bounded asynchronous export and local drop accounting. Customer requests complete from authoritative state.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How does the service contain dependency failure without amplifying it, lying about success, or collapsing unrelated journeys?” is decided by durable state rather than telemetry?
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

These are the smallest useful entry points for **Dependency Resilience and Graceful Degradation**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/circuit.py`

```text
# Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
from .clock import Clock


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half-open"


class CircuitOpen(RuntimeError):
    pass


@dataclass(slots=True)
class CircuitBreaker:
    failure_threshold: int
    open_duration_ms: int
    half_open_max_calls: int = 1
    state: CircuitState = CircuitState.CLOSED
    consecutive_failures: int = 0
    opened_at_ms: int | None = None
    half_open_in_flight: int = 0

    def __post_init__(self) -> None:
        if self.failure_threshold < 1:
            raise ValueError("failure_threshold must be positive")
        if self.open_duration_ms < 1:
            raise ValueError("open_duration_ms must be positive")
        if self.half_open_max_calls < 1:
            raise ValueError("half_open_max_calls must be positive")

    def allow(self, clock: Clock) -> None:
        if self.state is CircuitState.OPEN:
            assert self.opened_at_ms is not None
            if clock.now_ms() - self.opened_at_ms < self.open_duration_ms:
                raise CircuitOpen("dependency circuit is open")
            self.state = CircuitState.HALF_OPEN
            self.half_open_in_flight = 0
        if self.state is CircuitState.HALF_OPEN:
            if self.half_open_in_flight >= self.half_open_max_calls:
                raise CircuitOpen("half-open probe already in flight")
            self.half_open_in_flight += 1

    def success(self) -> None:
        self.state = CircuitState.CLOSED
        self.consecutive_failures = 0
        self.opened_at_ms = None
        self.half_open_in_flight = 0

    def failure(self, clock: Clock) -> None:
        if self.state is CircuitState.HALF_OPEN:
            self._open(clock)
            return
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.failure_threshold:
            self._open(clock)

    def abandon_probe(self, clock: Clock) -> None:
        """Reopen after a canceled or abandoned half-open probe.

        Without this explicit path, cancellation can consume the only probe
        permit forever and make the circuit appear permanently unavailable.
        """

        if self.state is CircuitState.HALF_OPEN and self.half_open_in_flight:
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/circuit.ts`

```text
// Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
import type { Clock } from "./clock.js";

export type CircuitState = "closed" | "open" | "half-open";
export class CircuitOpen extends Error {}

export class CircuitBreaker {
  public state: CircuitState = "closed";
  public consecutiveFailures = 0;
  public openedAtMs: number | undefined;
  public halfOpenInFlight = 0;

  public constructor(
    public readonly failureThreshold: number,
    public readonly openDurationMs: number,
    public readonly halfOpenMaxCalls = 1,
  ) {
    if (!Number.isSafeInteger(failureThreshold) || failureThreshold < 1) {
      throw new Error("failureThreshold must be positive");
    }
    if (!Number.isSafeInteger(openDurationMs) || openDurationMs < 1) {
      throw new Error("openDurationMs must be positive");
    }
    if (!Number.isSafeInteger(halfOpenMaxCalls) || halfOpenMaxCalls < 1) {
      throw new Error("halfOpenMaxCalls must be positive");
    }
  }

  public allow(clock: Clock): void {
    if (this.state === "open") {
      if (this.openedAtMs === undefined) throw new Error("open circuit lacks timestamp");
      if (clock.nowMs() - this.openedAtMs < this.openDurationMs) {
        throw new CircuitOpen("dependency circuit is open");
      }
      this.state = "half-open";
      this.halfOpenInFlight = 0;
    }
    if (this.state === "half-open") {
      if (this.halfOpenInFlight >= this.halfOpenMaxCalls) {
        throw new CircuitOpen("half-open probe already in flight");
      }
      this.halfOpenInFlight += 1;
    }
  }

  public success(): void {
    this.state = "closed";
    this.consecutiveFailures = 0;
    this.openedAtMs = undefined;
    this.halfOpenInFlight = 0;
  }

  public failure(clock: Clock): void {
    if (this.state === "half-open") {
      this.open(clock);
      return;
    }
    this.consecutiveFailures += 1;
    if (this.consecutiveFailures >= this.failureThreshold) this.open(clock);
  }

  public abandonProbe(clock: Clock): void {
    if (this.state === "half-open" && this.halfOpenInFlight > 0) this.open(clock);
  }

  private open(clock: Clock): void {
```

Compare the two tracks by this invariant: **circuits, bulkheads, retry policy, and degradation apply per dependency and never convert uncertain durable outcomes into success**. The intended implementation difference is: state-machine mechanics differ; open, half-open, probe, and recovery decisions are shared.

## Module synthesis

You are ready to leave this module when you can **Classify dependency failures and ownership, Use bulkheads to bound local resource consumption, and Design circuit state and half-open probe ownership** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Inject artifact failure and plant false-success fallback** and requiring the following oracle: **API reads remain available during webhook saturation; Collector outage causes drop evidence, not response failure; No completed run lacks artifact evidence; Half-open concurrency stays bounded.**

The cumulative platform now includes **Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Lifecycle, Health, Shutdown, and Recovery](../module-04-lifecycle-health-graceful-shutdown-and-recovery/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
