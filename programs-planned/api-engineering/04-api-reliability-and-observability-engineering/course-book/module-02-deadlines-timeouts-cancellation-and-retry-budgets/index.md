# Module 02 — Deadlines, Cancellation, and Retry Budgets

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Central question:** How is one absolute time budget propagated through retries, dependencies, and cancellation without multiplying work?

## Where this module fits

Module 01 produced **Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims**. This module extends that result by asking: **How is one absolute time budget propagated through retries, dependencies, and cancellation without multiplying work?**

The new capstone increment is **Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation**. It becomes the prerequisite for **Dependency Resilience and Graceful Degradation**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish absolute deadlines from per-call timeouts.
- Budget connect, pool, transaction, read, write, and cleanup waits.
- Preserve committed durable work after caller cancellation.
- Retry only safe or idempotent effects.
- Use bounded backoff, jitter, and `Retry-After` inside the remaining budget.

## Capstone increment

Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation.

## Core reliability model

### Driving question

> How does one request carry a finite time budget through every dependency without multiplying work or reporting success after the caller has left?

A timeout limits one wait; a deadline bounds the whole operation. Retries are allowed only inside the remaining deadline and only when duplicate effects are controlled.

### 1. Absolute deadline

An absolute expiry survives nested calls and prevents each layer from resetting a full timeout. It is computed once at the boundary and converted into smaller child budgets.

**Failure if confused.** Three nested five-second timeouts can consume fifteen seconds; one five-second deadline cannot.
### 2. Timeout scope

Connect, read, write, pool acquisition, transaction, idle, and total-operation timeouts protect different waits.

**Failure if confused.** A two-second read timeout does not prevent ten seconds waiting for a pool connection.
### 3. Cancellation

Cancellation says work may no longer be useful. It does not automatically roll back a committed transaction or revoke durable work.

**Failure if confused.** A disconnected HTTP client cannot erase a run already accepted and committed.
### 4. Retry safety

The same transient failure may be retryable for GET but unsafe for a mutation lacking idempotency. Safety is about effects, not only status code.

**Failure if confused.** Retrying a timed-out POST can create two runs if the first commit succeeded and its response was lost.
### 5. Retry budget

Attempts, delays, minimum execution time, and server guidance share the parent deadline rather than receiving fresh time at every layer.

**Failure if confused.** Client, API, and worker each retrying three times can create twenty-seven dependency calls.
### 6. Backoff and jitter

Backoff reduces pressure; jitter prevents synchronized callers. Deterministic seeds are testing devices, not a cross-language wire contract.

**Failure if confused.** Python and TypeScript can implement full jitter correctly while producing different seeded sequences.
### 7. Retry ownership

Exactly one layer owns automatic retry for a dependency call; others expose classified failure and remaining budget.

**Failure if confused.** An HTTP library and application loop must not both retry one webhook attempt.

For a new Analysis Runs failure:

Apply **Absolute deadline, Timeout scope, Cancellation** to this module’s capstone increment: Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Create deadline at ingress | Derive one absolute deadline from trusted configuration or a bounded internal propagation profile. | Relative timeout reset: Nested operations exceed caller budget | `deadline vectors` |
| 2 | Child cannot outlive parent | Every child expiry is the minimum of parent expiry and local maximum. | Retry unsafe mutation: Duplicate durable effects | `child-deadline tests` |
| 3 | Reserve execution time | Do not sleep when delay plus minimum attempt time exceeds remaining budget. | Sleep beyond deadline: Late useless failure | `deadline-fit tests` |
| 4 | Classify safety first | Unsafe mutations are never automatically retried without idempotency. | Multiple retry owners: Amplified dependency traffic | `retry matrix` |
| 5 | Honor Retry-After as bounded guidance | A valid value may delay a retry but cannot extend the deadline or make an unsafe operation retryable. | Ignore Retry-After: Dependency overload worsens | `header vectors` |
| 6 | Assign one retry owner | Dependency policy names owner and maximum attempts. | Trust arbitrary caller deadline: Caller forces unbounded or zero budget | `dependency-policies.yaml` |
| 7 | Cancellation cannot invent rollback | Committed work follows domain cancellation semantics after client disconnect. | Treat disconnect as rollback: Accepted work disappears | `disconnect scenario` |
| 8 | Record attempt evidence | Distinguish original calls, retries, exhaustion, and abandoned attempts without identifier labels. | Hide retries in latency: Slow requests are unexplained | `attempt metrics` |


### Evidence boundary

Injected clocks and deterministic retries prove budget arithmetic; they do not establish operating-system socket cancellation or intermediary retry behavior.

## Worked failures

### Case 1 — Timeout multiplication

#### Initial system

The API grants PostgreSQL, artifact storage, and webhook delivery five seconds each in sequence, so a nominal five-second request can consume fifteen seconds.


#### Correct design

Create a five-second absolute ingress deadline. Each child gets the lesser of remaining time and dependency maximum, with time reserved for cleanup and response.


#### Lesson

Independent local timeouts are necessary but insufficient.
### Case 2 — Lost response after commit

#### Initial system

The client times out after the server commits a run but before receiving 202. Blind retry creates a duplicate.


#### Correct design

Retry only with the Course 2 durable idempotency key. The same key replays committed outcome; changed body conflicts.


#### Lesson

A transport timeout does not reveal whether an effect happened.
### Case 3 — Retry storm

#### Initial system

Generated client, API, worker, and storage adapter each retry three times, multiplying one request into many calls.


#### Correct design

Name one retry owner nearest the dependency, cap attempts, propagate exhaustion, and measure amplification.


#### Lesson

Retries are load, not free resilience.
### Case 4 — Disconnect during accepted work

#### Initial system

The connection closes after durable acceptance. Cancelling the server task and deleting the job violates the 202 contract.


#### Correct design

Finish the transaction and allow durable work to continue. Explicit domain cancellation uses the cancellation operation.


#### Lesson

Transport cancellation and domain cancellation are different.

## Python implementation

### Mechanism under review

Use an injected clock; test exact boundaries without sleeps and inspect Retry-After parsing.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/deadline.py`
- `capstone/tracks/python-fastapi/src/api_reliability/retry.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_context_deadline.py`

### Executable invariant

```python
from api_reliability.clock import ManualClock
from api_reliability.deadline import Deadline
from api_reliability.retry import fit_delays_to_deadline

clock = ManualClock(1_000)
deadline = Deadline.after(clock, 600)
assert fit_delays_to_deadline(
    [100, 200, 400], clock=clock, deadline=deadline, minimum_attempt_ms=125
) == [100, 200]
```

The cited files must expose the complete **Deadlines, Cancellation, and Retry Budgets** implementation path and its negative regression evidence.

### Guided failure investigation — Timeout multiplication

**Initial condition.** The API grants PostgreSQL, artifact storage, and webhook delivery five seconds each in sequence, so a nominal five-second request can consume fifteen seconds.

**Expected repair.** Create a five-second absolute ingress deadline. Each child gets the lesser of remaining time and dependency maximum, with time reserved for cleanup and response.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=02 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Relative timeout reset.** Nested operations exceed caller budget The decisive check is absolute expiry assertion.
- **Retry unsafe mutation.** Duplicate durable effects The decisive check is idempotency and attempt audit.
- **Sleep beyond deadline.** Late useless failure The decisive check is deadline-fit test.
- **Multiple retry owners.** Amplified dependency traffic The decisive check is attempt-count experiment.
- **Ignore Retry-After.** Dependency overload worsens The decisive check is header parsing vectors.
- **Trust arbitrary caller deadline.** Caller forces unbounded or zero budget The decisive check is boundary clamp test.

## TypeScript implementation

### Mechanism under review

Use bigint-safe absolute times where needed and compare policy rather than pseudo-random sequence identity.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/deadline.ts`
- `capstone/tracks/typescript-fastify/src/reliability/retry.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/retry-circuit.test.mjs`

### Executable invariant

```typescript
const clock = new ManualClock(1_000);
const deadline = Deadline.after(clock, 600);
const fitted = fitDelaysToDeadline(
  [100, 200, 400],
  { clock, deadline, minimumAttemptMs: 125 },
);
if (JSON.stringify(fitted) !== "[100,200]") throw new Error("budget leak");
```

The cited files must expose the complete **Deadlines, Cancellation, and Retry Budgets** implementation path and its negative regression evidence.

### Guided failure investigation — Timeout multiplication

**Initial condition.** The API grants PostgreSQL, artifact storage, and webhook delivery five seconds each in sequence, so a nominal five-second request can consume fifteen seconds.

**Expected repair.** Create a five-second absolute ingress deadline. Each child gets the lesser of remaining time and dependency maximum, with time reserved for cleanup and response.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=02 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Relative timeout reset.** Nested operations exceed caller budget The decisive check is absolute expiry assertion.
- **Retry unsafe mutation.** Duplicate durable effects The decisive check is idempotency and attempt audit.
- **Sleep beyond deadline.** Late useless failure The decisive check is deadline-fit test.
- **Multiple retry owners.** Amplified dependency traffic The decisive check is attempt-count experiment.
- **Ignore Retry-After.** Dependency overload worsens The decisive check is header parsing vectors.
- **Trust arbitrary caller deadline.** Caller forces unbounded or zero budget The decisive check is boundary clamp test.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Relative timeout reset** | Each function can conveniently start its own timeout. | Nested calls exceed the caller’s total budget. | Single-dependency tests never compose enough layers to expose multiplication. | absolute expiry assertion. |
| **Retry unsafe mutation** | Transient failures encourage generic retry wrappers. | A non-idempotent effect can be applied more than once. | The happy path has no ambiguous response after a committed mutation. | idempotency and attempt audit. |
| **Sleep beyond deadline** | Backoff is calculated without rechecking remaining budget. | The caller waits after useful work is already impossible. | Fast failures leave enough budget, so the error appears harmless. | deadline-fit test. |
| **Multiple retry owners** | Every layer tries to be helpful independently. | Attempts multiply and overload the failing dependency. | Unit tests inspect one owner at a time and miss amplification. | attempt-count experiment. |
| **Ignore Retry-After** | Local backoff code is simpler than parsing server guidance. | Clients retry sooner than the dependency can recover or later than the caller can wait. | The normal dependency response does not include throttling guidance. | header parsing vectors. |
| **Trust arbitrary caller deadline** | Forwarding caller metadata appears transparent. | An untrusted value can force unreasonable resource use or bypass local caps. | Trusted test clients send well-formed, moderate values. | boundary clamp test. |
| **Treat disconnect as rollback** | The client disappeared, so it is tempting to assume the operation disappeared. | Durable work may have committed and later retry can duplicate intent. | Happy paths keep the connection open through the response. | durable job oracle. |
| **Hide retries in latency** | Reporting only final service time makes the dependency look healthy. | Queue and retry delay vanish from the user experience. | A test with no retry has identical final and total latency. | attempt and delay telemetry. |

## What you add to the capstone

### Increment

Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/deadline.py`
- `capstone/tracks/python-fastapi/src/api_reliability/retry.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_context_deadline.py`
- `capstone/tracks/typescript-fastify/src/reliability/deadline.ts`
- `capstone/tracks/typescript-fastify/src/reliability/retry.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/retry-circuit.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Create deadline at ingress.** Derive one absolute deadline from trusted configuration or a bounded internal propagation profile.
- **Child cannot outlive parent.** Every child expiry is the minimum of parent expiry and local maximum.
- **Reserve execution time.** Do not sleep when delay plus minimum attempt time exceeds remaining budget.
- **Classify safety first.** Unsafe mutations are never automatically retried without idempotency.
- The planted failure **Timeout multiplication** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Timeout multiplication**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Create a five-second absolute ingress deadline. Each child gets the lesser of remaining time and dependency maximum, with time reserved for cleanup and response.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How does one request carry a finite time budget through every dependency without multiplying work or reporting success after the caller has left?” is decided by durable state rather than telemetry?
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

These are the smallest useful entry points for **Deadlines, Cancellation, and Retry Budgets**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/deadline.py`

```python
from .clock import Clock


class DeadlineExceeded(TimeoutError):
    pass


@dataclass(frozen=True, slots=True)
class Deadline:
    expires_at_ms: int

    @classmethod
    def after(cls, clock: Clock, timeout_ms: int) -> "Deadline":
        if timeout_ms <= 0:
            raise ValueError("timeout must be positive")
        return cls(clock.now_ms() + timeout_ms)

    def remaining_ms(self, clock: Clock) -> int:
        return max(0, self.expires_at_ms - clock.now_ms())

    def expired(self, clock: Clock) -> bool:
        return self.remaining_ms(clock) == 0

    def require_remaining(self, clock: Clock, minimum_ms: int = 1) -> int:
        remaining = self.remaining_ms(clock)
        if remaining < minimum_ms:
            raise DeadlineExceeded("operation deadline exhausted")
        return remaining

    def child(self, clock: Clock, maximum_ms: int) -> "Deadline":
        if maximum_ms <= 0:
            raise ValueError("child maximum must be positive")
        return Deadline(min(self.expires_at_ms, clock.now_ms() + maximum_ms))
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/deadline.ts`

```typescript
import type { Clock } from "./clock.js";

export class DeadlineExceeded extends Error {}

export class Deadline {
  public constructor(public readonly expiresAtMs: number) {
    if (!Number.isSafeInteger(expiresAtMs)) throw new Error("deadline must be a safe integer");
  }
  public static after(clock: Clock, timeoutMs: number): Deadline {
    if (!Number.isSafeInteger(timeoutMs) || timeoutMs <= 0) throw new Error("timeout must be positive");
    return new Deadline(clock.nowMs() + timeoutMs);
  }
  public remainingMs(clock: Clock): number { return Math.max(0, this.expiresAtMs - clock.nowMs()); }
  public requireRemaining(clock: Clock, minimumMs = 1): number {
    const remaining = this.remainingMs(clock);
    if (remaining < minimumMs) throw new DeadlineExceeded("operation deadline exhausted");
    return remaining;
  }
  public child(clock: Clock, maximumMs: number): Deadline {
    if (maximumMs <= 0) throw new Error("child maximum must be positive");
    return new Deadline(Math.min(this.expiresAtMs, clock.nowMs() + maximumMs));
  }
}
```

Compare the two tracks by this invariant: **one caller budget is partitioned across attempts and dependencies without resetting at each layer or retrying unsafe effects**. The intended implementation difference is: clock and cancellation APIs differ; remaining time and retry eligibility must match.

## Module synthesis

You are ready to leave this module when you can **Distinguish absolute deadlines from per-call timeouts, Budget connect, pool, transaction, read, write, and cleanup waits, and Preserve committed durable work after caller cancellation** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a loop resetting timeout per attempt** and requiring the following oracle: **No child exceeds parent expiry; Unsafe POST gets one attempt; Delay plus minimum attempt fits remaining time; Attempt count matches named owner policy.**

The cumulative platform now includes **Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Dependency Resilience and Graceful Degradation](../module-03-dependency-resilience-and-graceful-degradation/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
