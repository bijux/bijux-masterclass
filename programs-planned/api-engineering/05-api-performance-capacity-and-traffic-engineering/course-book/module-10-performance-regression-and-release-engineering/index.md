# Module 10 — Performance Regression and Release Engineering

> **Program stage:** Course 5 of 6 — Sustain the promise under pressure.

> **Central question:** How does a performance change become a reproducible release decision rather than a favorable chart?

## Where this module fits


A performance course is incomplete if it ends with a tuning report. Real systems change continuously. Dependencies, compilers, data scale, indexes, configuration, and traffic mix can erase a gain or introduce a regression months later. Performance engineering therefore needs a release process.

A good regression gate is strict about identity and correctness but cautious about noisy latency. It does not fail every build because one shared runner was busy, and it does not ignore a material tail regression because the mean improved. It uses tiered evidence: deterministic mechanism tests on every change, controlled workload comparisons on selected changes, and representative environment validation before consequential releases.

This final module assembles the performance dossier. The learner must accept one candidate, reject one faster-but-invalid candidate, and classify one result as insufficient evidence. The ability to refuse a misleading result is part of mastery.


## Capstone result

Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier.

Publish performance profile 1.0, an accepted release, a deliberately rejected regression candidate, CI comparison logic, rollback triggers, and the sanitized Course 6 handoff.

## Learning outcomes

By the end of this module, you can:

- design a tiered performance verification pipeline
- enforce identity and correctness before metric comparison
- combine absolute and relative regression thresholds
- handle noise through run series and inconclusive decisions
- select stable mechanism-level CI tests
- avoid brittle wall-clock gates on uncontrolled runners
- write release acceptance, rollback, and remeasurement criteria
- connect performance alerts and capacity triggers to operations
- produce a reviewable performance dossier
- sanitize and manifest the next-course handoff

## Core performance model

### 1. Performance release dossier


A decision-grade dossier contains:

```text
change and hypothesis
inherited version/profile proof
workload and environment identities
baseline run series
candidate run series
correctness outcomes
latency/throughput/resource summaries
query/runtime/cache/traffic evidence
capacity impact
trade-offs and residual risks
accept/reject/inconclusive decision
rollback and remeasurement triggers
```

This is not a slide deck. It is a machine-readable record plus a concise engineering explanation. Another engineer should be able to reproduce the comparison or identify why they cannot.


### 2. Tiered verification


Run the cheapest deterministic checks frequently and expensive representative checks deliberately:

### Tier 1 — every change

- pure statistics and policy vectors;
- schema and manifest checks;
- output conformance;
- planted-defect sensitivity;
- algorithmic complexity or operation-count bounds where stable.

### Tier 2 — local process

- local HTTP workloads;
- runtime profiling smoke;
- cache/concurrency burst tests;
- short benchmark comparison.

### Tier 3 — live dependencies

- PostgreSQL plans and write cost;
- process/worker/storage topology;
- longer run series.

### Tier 4 — representative pre-release

- production-like data, resources, topology, and workload;
- capacity/degraded scenarios;
- release and rollback rehearsal.

Do not run a noisy five-minute wall-clock gate on every shared CI worker and call it rigor.


### 3. Comparison order


The capstone release evaluator applies:

1. workload/build/environment comparability;
2. predecessor and profile integrity;
3. correctness and security;
4. outcome coverage and error/rejection budgets;
5. latency, throughput, and resource thresholds;
6. capacity and residual-risk review.

A failure at an earlier stage prevents approval at later stages. The evaluator may still report metrics for diagnosis, but the decision remains rejected.

This order blocks a candidate that omits telemetry, drops errors, or changes the workload from advertising a performance win.


### 4. Absolute and relative thresholds


Use both:

```text
regression if:
  candidate_p95 - baseline_p95 > absolute_ms
  AND
  (candidate_p95 / baseline_p95 - 1) > relative_fraction
```

The exact Boolean policy may vary. Requiring both can prevent tiny absolute noise near zero; requiring either can be stricter. State the rule.

Resource gates may use maximum absolute budgets, such as memory under 512 MiB, and relative service-demand budgets, such as no more than 5% CPU/request increase. Throughput improvements require correctness and a practical minimum.


### 5. Noise and inconclusive results


A release evaluator needs a third state:

```text
accepted
rejected
inconclusive
```

If environment fingerprints differ, run variance is too large, sample coverage is insufficient, or the result straddles the decision threshold, mark inconclusive and rerun in a controlled environment.

Forcing every result into pass/fail rewards false certainty. Inconclusive is not a free pass; it blocks the performance claim while allowing unrelated correctness work according to project policy.


### 6. Stable CI oracles


Use deterministic or bounded-work tests for every change:

- range parser does not read more than selected bytes;
- cache stampede makes one origin call;
- waiter count never exceeds limit;
- SQL query retains mandatory predicates;
- plan fixture contains no forbidden scan/spill under declared data;
- serialization produces equivalent output and no redundant conversion call;
- release evaluator rejects wrong workload hash.

These tests catch mechanism regressions without depending on exact wall time. Use wall-clock budgets only in controlled, dedicated runners with sufficient repetition.


### 7. Baseline lifecycle


A baseline is versioned and immutable once accepted. Replacing it requires a reason:

- intended software or configuration release;
- representative environment change;
- workload or data-distribution version;
- corrected benchmark defect;
- revised service objective.

Do not “update the baseline” merely because a candidate failed. Keep lineage: old baseline, candidate, accepted new baseline, and decision.

Baseline aging is real. Schedule remeasurement when data size, runtime, dependency, index, topology, or traffic mix changes materially.


### 8. Release and rollback


Performance changes can affect correctness under load even when functional tests pass. A release plan identifies:

- feature flag or reversible configuration where possible;
- migration dependency;
- canary or staged exposure;
- metrics and SLI populations to compare;
- abort thresholds;
- rollback safety;
- cache/connection/worker state after rollback.

A database index may remain after application rollback; this can be safe but affects write cost. A cache-key format change may require dual read or natural expiry. Traffic-policy changes need profile/version awareness.


### 9. Operational feedback


Course 4 alerts detect service outcomes. Course 5 adds capacity and performance triggers, but does not replace SLOs with benchmark numbers.

Examples:

- queue wait approaches admission deadline;
- p95 resource demand regresses after release;
- database buffer reads per list page exceed budget;
- active stream permits stay saturated;
- cache miss origin calls spike;
- forecast headroom falls below threshold.

A trigger names the workload/population and runbook action. Avoid high-cardinality metric labels derived from workload IDs or tenants without governance.


### 10. Planted defects and proof sensitivity


A proof suite that never fails might be checking nothing. The course packages ten planted defects:

1. workload ID not hash-bound;
2. coordinated omission;
3. range off-by-one;
4. owner predicate removed;
5. async blocking;
6. permit leak;
7. tenant omitted from cache key;
8. partial token charge;
9. backlog drain formula accepts `μ <= λ`;
10. release evaluator checks latency before correctness.

The sensitivity route activates each defect in isolation and requires the corresponding proof to fail for the intended reason.


### 11. Handoff discipline


Course 6 needs measured queue, worker, and traffic budgets to design asynchronous messaging. It does not need raw production identifiers, secrets, full benchmark event logs, or machine-specific paths.

The handoff includes stable profiles, workload catalogue, accepted capacity model, migration 009, and sanitized benchmark envelopes. It has its own manifest. The receiving course verifies it before changing communication architecture.


## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Tiered proof | Deterministic and environment-backed checks are separated. | Noisy shared CI becomes false authority. | Pipeline definition |
| Early-gate precedence | Identity/correctness/coverage precede speed. | Fast wrong candidate passes. | Release evaluator tests |
| Thresholds versioned | Absolute/relative/resource rules are fixed before candidate. | Gate moves after result. | Performance profile |
| Inconclusive supported | Noise or mismatch blocks claim without fabricated pass/fail. | Uncertain result is forced to victory. | Decision state |
| Baseline immutable | Accepted baseline has lineage and replacement reason. | Failed candidate rewrites history. | Baseline registry |
| Rollback measurable | Abort conditions and post-rollback state are defined. | Release can regress service without safe exit. | Release plan |
| Proof sensitivity | Each critical proof rejects a planted defect. | Green suite checks only happy path. | Sensitivity report |
| Handoff sanitized | Next course receives necessary profiles, not secrets or ephemeral data. | Internal evidence leaks or lineage is lost. | Manifest and scanner |

## Worked failures

### Case 1 — The faster wrong release

**Initial condition.** Candidate p95 improves 25%, but idempotency replay returns a new response body and errors are excluded.

**Analysis.** Correctness and population changed. Performance comparison is invalid.

**Correct response.** Reject at early gates, retain metrics only for diagnosis, and repair semantics.

**Lesson.** Release order matters.

### Case 2 — The flaky CI budget

**Initial condition.** A shared CI runner fails when p95 exceeds 50 ms; results vary 30–90 ms with no environment fingerprint.

**Analysis.** Runner contention dominates and the threshold is not reproducible.

**Correct response.** Use deterministic mechanism gates in shared CI and a controlled performance runner for latency.

**Lesson.** Strict-looking gates can be meaningless.

### Case 3 — The baseline rewrite

**Initial condition.** Candidate regresses 12%, so the team replaces the baseline with the candidate and declares no change.

**Analysis.** Historical decision evidence is destroyed.

**Correct response.** Keep immutable lineage, reject or approve with explicit budget/requirement change.

**Lesson.** A baseline is a versioned decision record.

### Case 4 — The confident overlap

**Initial condition.** Run-level intervals overlap the threshold and environments differ slightly, but the report chooses the lower candidate median.

**Analysis.** The evidence cannot support the claim.

**Correct response.** Mark inconclusive and rerun under matched, controlled conditions.

**Lesson.** Refusing certainty is an engineering outcome.

## Python implementation

### Mechanism

The Python release module validates comparability, correctness, coverage, thresholds, and capacity impact in fixed order and emits accepted/rejected/inconclusive findings.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/release.py`
- `capstone/tracks/python-fastapi/src/api_performance/regression.py`
- `capstone/tracks/python-fastapi/tests_performance/test_release_regression.py`

### Focused example

```python
from api_performance.release import evaluate_release

decision = evaluate_release(baseline, candidate, policy)
assert decision.status in {"accepted", "rejected", "inconclusive"}
assert decision.gates[0].name == "comparability"
assert decision.gates[1].name == "correctness"
```

The evaluator returns every gate with evidence and does not short-circuit reporting, but approval cannot proceed past an earlier failed gate. Decimal thresholds and named metric populations prevent ambiguous arithmetic.

### Python-specific failure to avoid

Do not use nondeterministic dict iteration or current time inside release decisions. Timestamps belong to the report envelope; the same inputs must produce the same decision.

## TypeScript implementation

### Mechanism

The TypeScript evaluator consumes the same JSON envelopes and policy, preserves decimal/count boundaries, and produces byte-stable normalized findings.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/release.ts`
- `capstone/tracks/typescript-fastify/src/performance/regression.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/release-regression.test.mjs`

### Focused example

```typescript
const decision = evaluateRelease(baseline, candidate, policy);
if (!["accepted", "rejected", "inconclusive"].includes(decision.status)) {
  throw new Error("invalid decision");
}
if (decision.gates[0].name !== "comparability") {
  throw new Error("wrong gate order");
}
```

The serializer sorts findings by fixed policy order, not object key order or timing. Shared vectors assert exact statuses and reason codes.

### TypeScript-specific failure to avoid

Avoid converting decimal-string thresholds and bigint counts to imprecise number values. The evaluator uses scaled integers or exact decimal helpers.

## Cross-language invariant

Both tracks make identical decisions and reason codes for accepted, rejected, and inconclusive vectors, including early correctness failure and environment mismatch.

## Failure patterns

- **Speed-first gate.** Latency is checked before correctness. **Decisive check:** gate-order vector.
- **Flaky shared runner.** Exact wall-time threshold on noisy host. **Decisive check:** tiered pipeline.
- **Baseline laundering.** Failed candidate becomes new baseline silently. **Decisive check:** immutable registry.
- **Pass/fail coercion.** Mismatched evidence is forced to a conclusion. **Decisive check:** inconclusive state.
- **Metric cherry-pick.** Mean improves while p95/resource/errors regress. **Decisive check:** multi-dimensional policy.
- **Proof insensitivity.** Planted defect leaves suite green. **Decisive check:** sensitivity report.

## Evidence and design review

Before accepting the module increment, answer:

1. Can another engineer reproduce the baseline and candidate?
2. Which early gate can reject the candidate before performance?
3. Are thresholds fixed and practically meaningful?
4. Does run variability support acceptance, rejection, or inconclusive?
5. What state remains after rollback?
6. Which planted defect proves each critical gate is sensitive?

## Module synthesis

Performance engineering becomes durable when it is part of release governance. Module 10 creates a correctness-first, reproducible, noise-aware pipeline and hands measured capacity constraints to the next course.

Proceed to [Exercises](exercises.md), then complete the [Lab](lab.md) and [Checkpoint](checkpoint.md).

## Next in the story

This course now has the mechanism needed for its final defense. The outgoing handoff becomes the immutable starting point for **Course 6 — Event-Driven API Engineering**, where the responsibility becomes: Design, evolve, secure, operate, and verify asynchronous contracts when delivery may be delayed, duplicated, reordered within declared limits, or replayed.
