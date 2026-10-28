# Module 09 — Fault Injection, Troubleshooting, and Game Days

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Central question:** How can fault injection and game days produce falsifiable evidence without creating uncontrolled damage?

## Where this module fits

Module 08 produced **Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy**. This module extends that result by asking: **How can fault injection and game days produce falsifiable evidence without creating uncontrolled damage?**

The new capstone increment is **Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects**. It becomes the prerequisite for **Incident Command, Reconciliation, and Readiness**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Predict the failure and first oracle before injection.
- Control blast radius and synthetic tenants.
- Diagnose from user journey to durable state to telemetry.
- Prove alerts and runbooks are sensitive to planted defects.
- Verify cleanup mechanically.

## Capstone increment

Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects.

## Core reliability model

### Driving question

> How do we test failure behavior deliberately, safely, and reproducibly—and diagnose from symptoms to mechanism instead of guessing from dashboards?

A reliability experiment begins with a steady-state claim and falsifiable hypothesis, injects one bounded fault, observes authoritative and diagnostic evidence, stops safely, cleans up, and retains a regression. Chaos without an oracle is disruption, not engineering.

### 1. Steady-state hypothesis

The experiment names what should remain true while the fault is active, using a journey SLI or durable invariant.

**Failure if confused.** “See what happens if the database is slow” has no pass condition.
### 2. Fault model

Latency, failure, connection drop, malformed response, resource exhaustion, clock shift, and process termination exercise different mechanisms.

**Failure if confused.** Returning 500 does not test a hung socket or partial write.
### 3. Blast radius

Scope is bounded by synthetic tenant, dependency, operation, duration, and concurrency.

**Failure if confused.** A global production fault to test one webhook retry is unjustified.
### 4. Abort condition

The experiment stops when safety, data integrity, resource bounds, or unrelated journeys exceed limits.

**Failure if confused.** Waiting for total outage before stopping defeats controlled learning.
### 5. Troubleshooting ladder

Start with the user journey and durable state, then narrow by timing, dependency, resource, and trace/log evidence.

**Failure if confused.** Opening random dashboards first encourages confirmation bias.
### 6. Counterfactual

A control or baseline shows whether the fault caused the observed change rather than normal variance.

**Failure if confused.** One slow request during injection does not prove causality.
### 7. Cleanup proof

Restoring configuration is not enough; verify fault disabled, queues drained or bounded, permits released, and state reconciled.

**Failure if confused.** A hidden latency proxy remains active after the exercise.
### 8. Regression retention

A discovered weakness becomes a deterministic test or verification, not only an incident note.

**Failure if confused.** The same lease-recovery defect returns in the next release.

For a new Analysis Runs failure:

Apply **Steady-state hypothesis, Fault model, Blast radius** to this module’s capstone increment: Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Write prediction before injection | Hypothesis, journey, fault, expected signals, oracle, stop, and cleanup are recorded first. | No hypothesis: Experiment produces anecdotes | `experiment plan check` |
| 2 | Inject one primary fault | Compound scenarios are introduced only after single-fault behavior is understood. | Wrong fault mechanism: Target behavior is never exercised | `fault profile review` |
| 3 | Bound blast radius | Synthetic scope, duration, concurrency, and data are explicit. | Global blast radius: Unrelated journeys fail | `game-day scenario validation` |
| 4 | Use authoritative oracles | Durable state/public behavior decides pass; telemetry supports diagnosis. | No abort threshold: Damage grows until manual panic | `fault report` |
| 5 | Define abort conditions | Automated or human stops protect integrity and unrelated journeys. | Telemetry-only oracle: Sampling changes pass/fail | `abort test` |
| 6 | Preserve a control | Baseline or unaffected journey distinguishes fault effect from ambient change. | No control population: Causality remains ambiguous | `counterfactual evidence` |
| 7 | Verify cleanup mechanically | No active fault, leaked permit, stale lease, temporary file, or unbounded backlog remains. | Incomplete cleanup: Later tests inherit fault | `cleanup proof` |
| 8 | Retain regression evidence | Every confirmed weakness becomes a test, vector, alert, or runbook change. | No retained regression: Defect recurs | `remediation map` |


### Evidence boundary

The local fault injector proves experiment controls; production blast radius, change approval, and emergency stop authority remain organizational responsibilities.

## Worked failures

### Case 1 — Database 500 instead of latency

#### Initial system

The team wants to validate deadline propagation but injects immediate 500 responses. Retries and circuit behavior run, yet no pool or child-deadline exhaustion occurs.


#### Correct design

Use a latency or connection-hold fault with bounded duration and observe remaining budgets, pool acquisition, cancellation, and request outcome.


#### Lesson

Fault fidelity must match the mechanism under test.
### Case 2 — Game day without stop

#### Initial system

A webhook receiver is slowed and backlog grows without a queue-age abort. The exercise consumes storage and affects unrelated tenants.


#### Correct design

Scope to a synthetic subscription, cap deliveries, set backlog and age stop conditions, and verify API/database bulkheads remain healthy.


#### Lesson

Learning does not justify uncontrolled accumulation.
### Case 3 — Dashboard-first diagnosis

#### Initial system

Operators see high CPU and immediately scale API replicas, but the root cause is workers repeatedly retrying a permanent artifact error.


#### Correct design

Begin from the failing run journey, inspect durable job attempts and failure class, then use traces/metrics to locate amplification.


#### Lesson

Symptoms do not establish mechanism.
### Case 4 — Cleanup by configuration

#### Initial system

The fault injector profile is set to healthy, but a held connection and acquired permit remain. Later tests fail intermittently.


#### Correct design

Verify active connection count, permits, leases, temporary files, queue age, and profile state. Restart only as a last explicit cleanup step.


#### Lesson

Cleanup has its own oracle.

## Python implementation

### Mechanism under review

Drive deterministic fault profiles with a manual clock, collect authoritative findings, and implement automatic abort/cleanup assertions.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/faults.py`
- `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_telemetry_reconcile.py`

### Executable invariant

```python
from api_reliability.faults import FaultPlan

plan = FaultPlan(
    identifier="worker-loss", hypothesis="a leased job is recovered safely",
    steady_state=("one durable run exists",), blast_radius="one synthetic run",
    abort_conditions=("duplicate terminal effect",),
    cleanup=("restore worker", "run reconciliation"),
)
plan.validate()
```

The cited files must expose the complete **Fault Injection, Troubleshooting, and Game Days** implementation path and its negative regression evidence.

### Guided failure investigation — Database 500 instead of latency

**Initial condition.** The team wants to validate deadline propagation but injects immediate 500 responses. Retries and circuit behavior run, yet no pool or child-deadline exhaustion occurs.

**Expected repair.** Use a latency or connection-hold fault with bounded duration and observe remaining budgets, pool acquisition, cancellation, and request outcome.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=09 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **No hypothesis.** Experiment produces anecdotes The decisive check is plan validation.
- **Wrong fault mechanism.** Target behavior is never exercised The decisive check is mechanism mapping.
- **Global blast radius.** Unrelated journeys fail The decisive check is scope guard.
- **No abort threshold.** Damage grows until manual panic The decisive check is stop-condition test.
- **Telemetry-only oracle.** Sampling changes pass/fail The decisive check is durable/public proof.
- **No control population.** Causality remains ambiguous The decisive check is baseline comparison.

## TypeScript implementation

### Mechanism under review

Apply equivalent seeded profiles and resource cleanup through promises/AbortSignal while preserving deterministic shared scenario decisions.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/faults.ts`
- `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

### Executable invariant

```typescript
const plan = new FaultPlan({
  id: "worker-loss", hypothesis: "a leased job is recovered safely",
  steadyState: ["one durable run exists"], blastRadius: "one synthetic run",
  abortConditions: ["duplicate terminal effect"],
  cleanup: ["restore worker", "run reconciliation"],
});
plan.validate();
```

The cited files must expose the complete **Fault Injection, Troubleshooting, and Game Days** implementation path and its negative regression evidence.

### Guided failure investigation — Database 500 instead of latency

**Initial condition.** The team wants to validate deadline propagation but injects immediate 500 responses. Retries and circuit behavior run, yet no pool or child-deadline exhaustion occurs.

**Expected repair.** Use a latency or connection-hold fault with bounded duration and observe remaining budgets, pool acquisition, cancellation, and request outcome.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=09 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **No hypothesis.** Experiment produces anecdotes The decisive check is plan validation.
- **Wrong fault mechanism.** Target behavior is never exercised The decisive check is mechanism mapping.
- **Global blast radius.** Unrelated journeys fail The decisive check is scope guard.
- **No abort threshold.** Damage grows until manual panic The decisive check is stop-condition test.
- **Telemetry-only oracle.** Sampling changes pass/fail The decisive check is durable/public proof.
- **No control population.** Causality remains ambiguous The decisive check is baseline comparison.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **No hypothesis** | Injecting random failure feels like realistic chaos. | The experiment cannot falsify a specific resilience claim. | Something fails, so the exercise appears successful. | plan validation. |
| **Wrong fault mechanism** | A convenient exception approximates a dependency outage. | The real timeout, queue, or partial-write behavior is never exercised. | The application still follows the expected error branch. | mechanism mapping. |
| **Global blast radius** | One switch creates obvious symptoms. | Unrelated tenants and control populations are damaged. | A single-user lab has no unaffected group. | scope guard. |
| **No abort threshold** | The experiment is expected to be short. | Escalating harm has no automatic stop condition. | The planned run ends before the risk appears. | stop-condition test. |
| **Telemetry-only oracle** | Faults are easiest to see in dashboards. | The experiment cannot establish durable user outcomes. | The telemetry path remains healthy. | durable/public proof. |
| **No control population** | All traffic receives the fault. | Natural variation cannot be distinguished from the injection. | The observed failure matches the operator’s expectation. | baseline comparison. |
| **Incomplete cleanup** | Removing the injection is treated as recovery. | Queues, leases, circuits, or derived state remain damaged. | The test stops before post-fault behavior is checked. | resource inventory. |
| **No retained regression** | The game day report is considered sufficient. | The same defect can return unnoticed. | The original exercise is not rerun in CI. | remediation proof. |

## What you add to the capstone

### Increment

Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/faults.py`
- `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_telemetry_reconcile.py`
- `capstone/tracks/typescript-fastify/src/reliability/faults.ts`
- `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Write prediction before injection.** Hypothesis, journey, fault, expected signals, oracle, stop, and cleanup are recorded first.
- **Inject one primary fault.** Compound scenarios are introduced only after single-fault behavior is understood.
- **Bound blast radius.** Synthetic scope, duration, concurrency, and data are explicit.
- **Use authoritative oracles.** Durable state/public behavior decides pass; telemetry supports diagnosis.
- The planted failure **Database 500 instead of latency** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Database 500 instead of latency**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Use a latency or connection-hold fault with bounded duration and observe remaining budgets, pool acquisition, cancellation, and request outcome.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How do we test failure behavior deliberately, safely, and reproducibly—and diagnose from symptoms to mechanism instead of guessing from dashboards?” is decided by durable state rather than telemetry?
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

These are the smallest useful entry points for **Fault Injection, Troubleshooting, and Game Days**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/faults.py`

```python
import random


class FaultKind(str, Enum):
    DELAY = "delay"
    ERROR = "error"
    DROP = "drop"
    CORRUPT = "corrupt"


@dataclass(frozen=True, slots=True)
class FaultRule:
    target: str
    kind: FaultKind
    probability: float
    delay_ms: int = 0
    error_code: str = "injected-failure"

    def __post_init__(self) -> None:
        if not 0 <= self.probability <= 1:
            raise ValueError("probability must be between zero and one")
        if self.delay_ms < 0:
            raise ValueError("delay cannot be negative")


@dataclass(slots=True)
class FaultInjector:
    rules: list[FaultRule]
    seed: int = 0
    _rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def decide(self, target: str) -> FaultRule | None:
        for rule in self.rules:
            if rule.target == target and self._rng.random() < rule.probability:
                return rule
        return None

@dataclass(frozen=True, slots=True)
class FaultPlan:
    identifier: str
    hypothesis: str
    steady_state: tuple[str, ...]
    blast_radius: str
    abort_conditions: tuple[str, ...]
    cleanup: tuple[str, ...]
    approved_environments: tuple[str, ...] = ("course", "test")

    def validate(self) -> None:
        if not self.identifier or len(self.identifier) > 80:
            raise ValueError("fault plan identifier must contain 1..80 characters")
        if len(self.hypothesis.strip()) < 12:
            raise ValueError("fault plan requires a falsifiable hypothesis")
        if not self.steady_state:
            raise ValueError("fault plan requires a steady-state definition")
        if not self.blast_radius.strip():
            raise ValueError("fault plan requires a blast radius")
        if not self.abort_conditions:
            raise ValueError("fault plan requires abort conditions")
        if not self.cleanup:
            raise ValueError("fault plan requires cleanup actions")
        if not self.approved_environments:
            raise ValueError("fault plan requires approved environments")
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/faults.ts`

```typescript
export type FaultKind = "delay" | "error" | "drop" | "corrupt";
export interface FaultRule { readonly target: string; readonly kind: FaultKind; readonly probability: number; readonly delayMs?: number; readonly errorCode?: string }
function rng(seed: number): () => number { let state = seed >>> 0; return () => { state = (Math.imul(1664525, state) + 1013904223) >>> 0; return state / 0x100000000; }; }
export class FaultInjector {
  private readonly random: () => number;
  public constructor(private readonly rules: readonly FaultRule[], seed = 0) { this.random = rng(seed); }
  public decide(target: string): FaultRule | undefined { return this.rules.find((rule) => rule.target === target && this.random() < rule.probability); }
}

export interface FaultPlanInput {
  readonly id: string;
  readonly hypothesis: string;
  readonly steadyState: readonly string[];
  readonly blastRadius: string;
  readonly abortConditions: readonly string[];
  readonly cleanup: readonly string[];
  readonly approvedEnvironments?: readonly string[];
}

export class FaultPlan {
  public constructor(public readonly input: FaultPlanInput) {}
  public validate(): void {
    if (this.input.id.length < 1 || this.input.id.length > 80) {
      throw new Error("fault plan identifier must contain 1..80 characters");
    }
    if (this.input.hypothesis.trim().length < 12) {
      throw new Error("fault plan requires a falsifiable hypothesis");
    }
    if (this.input.steadyState.length === 0) throw new Error("fault plan requires a steady-state definition");
    if (this.input.blastRadius.trim() === "") throw new Error("fault plan requires a blast radius");
    if (this.input.abortConditions.length === 0) throw new Error("fault plan requires abort conditions");
    if (this.input.cleanup.length === 0) throw new Error("fault plan requires cleanup actions");
    if ((this.input.approvedEnvironments ?? ["course", "test"]).length === 0) {
      throw new Error("fault plan requires approved environments");
    }
  }
}
```

Compare the two tracks by this invariant: **faults have hypotheses, blast-radius guards, abort conditions, cleanup, and an oracle that distinguishes the intended failure**. The intended implementation difference is: injection hooks differ; seed, target, fault decision, and cleanup evidence are shared.

## Module synthesis

You are ready to leave this module when you can **Predict the failure and first oracle before injection, Control blast radius and synthetic tenants, and Diagnose from user journey to durable state to telemetry** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant one missing alert or misleading dashboard panel and demonstrate detection** and requiring the following oracle: **API availability may remain healthy while run-start freshness fails; Durable accepted jobs remain present and recoverable; Telemetry loss reduces diagnosis quality but not correctness; Mitigation stops budget burn without duplicate completion.**

The cumulative platform now includes **Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Incident Command, Reconciliation, and Readiness](../module-10-incident-command-state-reconciliation-and-operational-readiness/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
