# Workbook — Module 90: Production Readiness, Capacity Planning, Rollouts, and Incident Learning

[Chapter](index.md) · [Laboratory](../../labs/module-10-production-readiness-review/README.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Production Readiness, Capacity Planning, Rollouts, and Incident Learning** has become a usable model rather than remembered vocabulary. Its governing question is: *What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?* Preserve your first prediction and record decisive facts in a **production decision record**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 89 — Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?**
3. Draw the smallest **production decision record** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### 1. Average versus peak capacity

Traffic averages 2,000 requests/s, peaks at 5,000, and failover may double one region’s share. A candidate sustains 6,000 requests/s in a short test. Is one instance ready? Build a capacity argument that includes headroom, duration, skew, and resource limits.

### 2. Below-saturation load test

A test stops at 70% of expected capacity and reports no errors. What critical behavior remains unknown? Design a safe saturation and recovery experiment.

### 3. Rollout bundle

A release changes binary, configuration defaults, dependency versions, and stored format simultaneously. Explain why rollback becomes ambiguous. Decompose the rollout.

### 4. Untested rollback

A runbook says “redeploy previous version,” but nobody has tested compatibility with current configuration/data. What evidence is missing?

### 5. Stale readiness evidence

The performance report was produced before a queue redesign and dependency update. Can it approve the current revision? Define evidence freshness and invalidation.

### 6. Incident closure

A memory incident is fixed by restarting the service and adding more RAM. Explain why this is not engineering closure. What model, code, test, signal, or limit should change?

## Part 2 — Diagnose and repair

### Case A — Capacity by benchmark maximum

The team divides peak load by maximum throughput and chooses the exact number of instances with no headroom. Repair the model for deployments, failover, maintenance, and variance.

### Case B — Canary without decision rules

A 5% canary runs for one hour. Nobody defined metrics, thresholds, or rollback authority. Design a staged decision table.

### Case C — Runbook by implementation detail

The runbook says “restart broker task if channel receiver closed.” Operators observe high rejection and stale snapshots, not task internals. Rewrite the runbook around symptoms and safe actions.

### Case D — Postmortem blame

An incident review concludes “engineer forgot a limit.” Convert this into system learning: why was the omission possible, invisible, and unrehearsed?

## Part 3 — Focused exercises

### Exercise 1 — Capacity model

Create a model for connections, queue slots, active ingestion, retained series, snapshot bytes, CPU service rate, memory, and one-region failover. Use checked arithmetic and state measured assumptions.

### Exercise 2 — Rollout ladder

Design stages: pre-production, one instance, small percentage, half fleet, full fleet. For each, define duration, traffic, required signals, stop/rollback criteria, and decision owner.

### Exercise 3 — Runbook

Write one runbook for “ingestion overload with rising queue wait.” Include detection, confirmation, immediate safety action, diagnosis branches, rollback/scaling choices, communication, and recovery verification.

### Exercise 4 — Incident drill

Design a controlled failure drill for a stuck broker, memory pressure, or bad release. Define expected signals, human actions, safety bounds, and artifacts to preserve.

### Exercise 5 — Evidence invalidation map

Create a change-to-evidence matrix. Rows should include parser semantics, dependency update, queue capacity, tracing schema, release profile, target platform, configuration schema, and rollout tooling. Columns should include functional tests, performance, capacity, observability, security, package/install, rollback, and incident drill. Mark which evidence becomes stale for each change and justify at least three non-obvious cells.

### Exercise 6 — Go/no-go memorandum

Write a one-page launch decision with four sections: supported claim, current evidence, explicit blockers or accepted risks, and rollback authority. The memorandum must name the exact artifact digest and configuration. Avoid adjectives such as “robust” or “production-grade” unless each is replaced by a measurable property and a scope. End with the first signal that would trigger rollback and the person or role authorized to make that decision.

### Interleaved reasoning pass

1. For **Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the production decision record.
2. For **Derive initial capacity and headroom from measured service demand, resource use, and burst policy**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the production decision record.
3. For **Distinguish load test, stress test, soak test, fault test, compatibility test, and rollback rehearsal**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the production decision record.
4. For **Design canary, staged, blue/green, or shadow rollout policies with objective promotion and rollback criteria**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the production decision record.

5. Identify one guarantee from an earlier course that a careless implementation of **Production Readiness, Capacity Planning, Rollouts, and Incident Learning** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build the [Production Readiness Review](../../labs/module-10-production-readiness-review/README.md). The review consumes current evidence for performance, reliability, observability, security, rollback, and incident practice. Duplicate, missing, stale, or failed evidence blocks deployment. Capacity arithmetic is checked, and the decision explains every blocker rather than returning one boolean.

### Laboratory acceptance trace

Before opening the reference implementation for **Production Readiness Review**, record:

- the public behavior that demonstrates **Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Finish MetricRail as an operated product:

- current performance and capacity report;
- memory and queue budget;
- observability/operator guide;
- threat and dependency review;
- deterministic artifact manifest;
- configuration contract;
- install/upgrade/rollback rehearsal;
- staged rollout plan;
- overload and failure drills;
- final architecture and limitations record.

Run the final review against the exact source revision and artifact. A green decision is not permanent; material changes invalidate related evidence.

### Capstone invariant trace

For the Module 90 MetricRail increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. Why is maximum measured throughput not safe capacity?
2. What does a saturation/recovery test reveal?
3. Why should rollout dimensions be separated?
4. What makes rollback credible?
5. How does evidence become stale?
6. Why should runbooks begin with symptoms?
7. What transforms an incident into durable learning?
8. State the strongest honest readiness claim for MetricRail and its remaining limits.

### Exercise 6 — Conduct a go/no-go capacity review

Given a projected peak of 18,000 records per second, a measured sustainable rate of 24,000, a p99 ingest objective of 40 ms, and a planned two-instance rollout, construct a capacity decision. Include headroom for one-instance loss, background snapshots, uneven tenants, and measurement uncertainty. State which metric triggers rollback, which evidence is authoritative during the canary, and what happens to accepted work during shutdown. Do not approve the release merely because average throughput exceeds forecast demand.

### Production-readiness acceptance gate

The final decision must connect product behavior to an operator action. Every alert needs an owner and runbook; every capacity claim needs a workload and environment; every rollout needs a stop condition and rollback path; every incident drill needs evidence that terminal work was accounted for. Readiness is a current, bounded claim about a named artifact in a named environment—not a permanent label attached to a repository.

### Closed-book defense

In five minutes, answer “What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?” using the **production decision record**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside MetricRail. A list of APIs without the deciding relationship is incomplete.
