# Module 90 Solutions — Production Readiness, Capacity Planning, Rollouts, and Incident Learning

[Workbook](workbook.md) · [Chapter](index.md) · [MetricRail guide](../capstone.md)

## Part 1 — Readiness reasoning

### 1. Average versus peak capacity

Six thousand requests/s is below the possible 10,000/s failover peak and the test duration may not expose memory growth, thermal effects, or skew. Safe instance count uses sustained capacity at accepted latency/error/memory, applies headroom, and survives deployment overlap and failure scenarios. Capacity is multidimensional: CPU throughput alone does not guarantee queues, memory, series cardinality, or dependencies remain within bounds.

### 2. Below-saturation load test

It does not reveal the knee, admission behavior, queue growth, tail-latency collapse, memory at full queues, recovery time, cancellation, or shutdown under backlog. Increase offered load in controlled steps past the knee until a safety threshold, verify explicit shedding and complete accounting, then reduce load and observe bounded recovery without restart.

### 3. Rollout bundle

When code, config, dependencies, and data format move together, a failure has multiple causes and the previous binary may not understand current state. Separate compatible preparatory changes, deploy code capable of both formats/configs, migrate gradually, then remove old compatibility later. Each step gets its own stop and rollback route.

### 4. Untested rollback

Evidence must show the retained previous artifact installs, starts with current or restored configuration, understands current data/schema or has a reverse migration, passes health/smoke, and can receive traffic within the rollback window. A prose command is not proof.

### 5. Stale readiness evidence

Queue design and dependency changes alter performance, capacity, failure, and supply-chain assumptions, so the old report cannot approve the current artifact. Evidence should bind to source revision, lockfile, configuration schema, workload/corpus, profile, and artifact digest. Material changes invalidate affected areas.

### 6. Incident closure

Restart and RAM reduce symptoms but do not explain cause. Closure requires a corrected memory model, reproduction or evidence, a bound/shrink policy or code repair, regression/load test, signal for recurrence, runbook update, and capacity review. The durable output is changed system knowledge.

## Part 2 — Plan repairs

### Case A

Use sustained—not peak—throughput at required tail latency and error rate. Reserve headroom for variability, deployment overlap, one-instance/zone failure, background work, and growth. Calculate minimum instances for failover load, then validate memory/queue/dependency dimensions. Avoid exact operation at the knee.

### Case B

Before canary, define expected baseline, primary health/SLO metrics, resource and error thresholds, minimum duration/volume, automatic/manual rollback criteria, and one decision owner. Stages advance only when evidence is current; absence of data is not success.

### Case C

Start: “Ingestion rejection rises and queue wait exceeds objective.” Immediate actions: verify scope, stop rollout, reduce admission or scale if safe. Diagnosis branches use broker health, active work, downstream wait, memory, and recent changes. Restart is a controlled last action with known data/availability effects. Recovery requires queue/latency/terminal accounting to return to normal.

### Case D

Ask why configuration allowed an unbounded value, tests did not exercise growth, observability did not expose retained state, review lacked a resource ledger, and rollback/runbook were unpracticed. Add schema validation, a hard limit, adversarial test, metric/alert, review checklist, and drill. The goal is not avoiding human error through blame but making the unsafe state difficult and visible.

## Part 3 — Model answers

### Exercise 1

A checked model combines:

```text
memory = fixed
       + connections × max_connection_state
       + queue_slots × max_message
       + active × max_active_state
       + series × max_series_state
       + snapshot_bound
       + measured runtime/allocator allowance
```

CPU capacity uses sustained completions at target tail latency under normal and skewed workloads. Failover demand includes peak plus region loss and deployment overlap. Every multiplication/addition is checked; measured terms cite workload/environment.

### Exercise 2

Pre-production proves functional, load, failure, and rollback behavior. One instance checks artifact/config/telemetry. Small percentage checks real distribution with strict stop rules. Half fleet checks capacity interactions and global dependencies. Full fleet proceeds only after stable windows. Each stage names duration/volume, metrics, capacity/error thresholds, rollback trigger, and accountable decision owner.

### Exercise 3

The overload runbook should include: alert symptoms; verify offered/admitted/completed/rejected and queue wait; inspect recent rollout and dependency state; stop progression; protect service through shedding or bounded scaling; branch on CPU saturation, downstream wait, hot-key skew, or memory; decide rollback; communicate impact; verify queue drains, tail latency and error budget recover, and every accepted request is terminal; preserve traces/config/artifact IDs.

### Exercise 4

For a stuck broker drill, inject a controlled pause on a noncritical environment, cap traffic/duration, predict readiness and overload signals, verify admission closes and requests terminate explicitly, follow the runbook, restore the broker, observe recovery, and preserve timeline, signals, actions, and unexpected gaps. A drill succeeds by revealing model defects, not by perfectly matching the script.

## Part 4 — Laboratory review

The review should require one unique evidence item per area, reject empty descriptions, distinguish missing/stale/failed evidence, and bind current/reviewed revisions. Failed evidence blocks even if stale. Capacity is checked for overflow and compared with the budget. The output explains blockers and estimated capacity rather than collapsing them into a boolean.

## Part 5 — MetricRail transfer

Every readiness artifact must match the final source, lockfile, profile, target, configuration, and digest. The rollout and rollback use retained packages. Overload/failure drills exercise actual signals and actions. The final record states limitations: reference-host measurements are not universal, process RSS is partly observed, network/kernel behavior depends on environment, and no static review proves absence of all vulnerabilities.

## Part 6 — Defense

Maximum throughput sits at or beyond unstable operation; safe capacity includes headroom and all resources. Saturation/recovery reveals shedding and whether the system returns to normal. Separating rollout dimensions improves attribution and rollback. Rollback is credible only after rehearsal with exact artifacts/state. Evidence stales when its bound inputs change. Symptom-first runbooks match operator knowledge. Incidents become learning when models, limits, tests, signals, or procedures change. The strongest honest claim is that MetricRail is a bounded, measured, diagnosable reference service under its declared workloads and environments—not that it is universally fast, secure, or production-ready for every deployment.
