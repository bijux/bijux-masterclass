# Module 90 — Production Readiness, Capacity Planning, Rollouts, and Incident Learning

**90/90** · Course 9 · Module 90 of 90

[Course 9 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [MetricRail guide](../capstone.md)

## The question

> What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?

## Why this comes now

The first nine modules produce local evidence: benchmarks, profiles, memory budgets, capacity curves, signal schemas, reliability policies, threat controls, and release identity. Module 90 assembles those pieces into a decision about real exposure. Production readiness is not another test command. It is a reasoned judgment about whether known risks are bounded, observable, reversible, and owned.

Capacity, rollout, rollback, and incident response must be designed together. A service can meet steady-state targets and still fail during deployment overlap, dependency degradation, burst traffic, or a configuration mistake.

## What you will be able to do

After completing this module, you will be able to:

- write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery
- derive initial capacity and headroom from measured service demand, resource use, and burst policy
- distinguish load test, stress test, soak test, fault test, compatibility test, and rollback rehearsal
- design canary, staged, blue/green, or shadow rollout policies with objective promotion and rollback criteria
- define configuration ownership, safe defaults, validation, dynamic-change policy, and auditability
- prepare runbooks that begin from symptoms and evidence rather than internal function names
- turn incidents and near misses into corrected models, tests, limits, and architecture rather than blame or one-off patches

## Core model

### The governing model

Production readiness is an evidence graph. Every claim points to a test, measurement, limit, runbook, or ownership decision. Use `artifact → configuration → workload envelope → dependencies → observability → failure policy → recovery → rollout → learning`. Unknowns are acceptable when named and bounded; invisible assumptions are not. A readiness review can reject deployment even when all unit tests pass.

### 1. Capacity is a model with headroom

Begin with measured per-request or per-record resource demand, concurrency, queue limits, retention, and dependency capacity. Translate expected traffic and burst shape into CPU, memory, network, storage, and connection demand. Add headroom for variance, failover, deployment overlap, and measurement error. State which resource saturates first.


### 2. Different tests answer different questions

A load test checks expected demand. A stress test crosses capacity to observe degradation and recovery. A soak test exposes leaks, retention, fragmentation, or time-dependent failure. Fault tests remove dependencies or delay operations. Compatibility tests cover versions and configuration. Rollback rehearsal proves the reverse path actually works.


### 3. Rollout as a controlled experiment

A canary exposes a small population to the new artifact. Staged rollout expands in steps. Blue/green maintains two environments for rapid switch. Shadow traffic exercises a path without serving its response. Each needs promotion criteria, observation windows, ownership, and automatic or manual rollback rules. Avoid changing code, configuration, and data format simultaneously.


### 4. Configuration is an API

Configuration has names, types, defaults, ranges, precedence, reload semantics, and security implications. Validate it before serving traffic. Reject unknown fields when silent typos are dangerous. Mark restart-required settings. Record changes without recording secrets. A safe default protects resources even when operators omit tuning.


### 5. Runbooks and incident command

A runbook starts from symptoms such as rising queue time, memory growth, dependency errors, or failed readiness. It points to authoritative signals, safe mitigations, rollback commands, and escalation ownership. During an incident, preserve a timeline and distinguish mitigation from diagnosis. Avoid speculative changes that destroy evidence.


### 6. Learning closes the course

A useful incident review identifies which model, limit, test, signal, or ownership assumption failed. Actions should change durable system evidence: add a bound, revise a contract, create a fault test, improve an alert, or simplify architecture. “Be more careful” is not a control. Re-run readiness when the architecture or operating envelope changes.

A readiness claim is a ledger of product contracts and evidence, each with scope and age. Evidence can become stale when code, configuration, workload, dependency, or infrastructure changes. The final review therefore checks not only whether evidence exists, but whether it applies to the exact artifact and operating envelope being proposed.

### A module-specific decision table

| Readiness area | Evidence | Release-blocking example |
|---|---|---|
| semantics | tests, invariants, compatibility cases | accepted data can be silently corrupted |
| performance | contract, benchmark, profile, load curve | p99 exceeds objective before expected load |
| resources | memory and capacity envelope | one valid request can exceed budget |
| overload | admission and terminal accounting | demand can accumulate without bound |
| observability | signal and diagnosis exercise | operator cannot distinguish overload from defect |
| security | threat model and control tests | unauthenticated exposure violates deployment boundary |
| release | artifact manifest and install test | running bytes cannot be tied to reviewed source |
| operations | rollout, rollback, runbook, incident drill | rollback has never been executed |

### Working procedure

1. Freeze the exact artifact, configuration, workload envelope, and deployment topology.
2. Build a claim-to-evidence ledger and reject stale or mismatched evidence.
3. Calculate capacity with burst, failover, rollout overlap, skew, and headroom.
4. Define staged exposure, observation windows, stop conditions, and automatic rollback signals.
5. Rehearse installation, migration, rollback, quiescing, and recovery.
6. Run an incident scenario using only documented signals and runbooks.
7. Accept only unknowns that are bounded, observable, reversible, and owned; record the experiment that will resolve them.

### Failure patterns and principled repairs

#### Treating a green test suite as sufficient production evidence.

Tests establish important semantics but do not model production load, topology, dependencies, or operator action. Complete the evidence ledger.

#### Calculating capacity from average traffic while ignoring burst, skew, failover, and deployment overlap.

Average traffic hides bursts, skew, failover, and deployment overlap. Capacity planning must include all four and preserve headroom.

#### Running a load test only below saturation and claiming overload behavior is understood.

A below-saturation test cannot reveal overload behavior. Cross the knee safely and observe rejection, memory, and recovery.

#### Rolling out code, configuration, dependency versions, and data format in one indivisible change.

Bundling code, configuration, dependency, and format changes destroys rollback clarity. Stage independent axes where possible.

#### Keeping rollback as a document that has never been executed.

An untested rollback is a hypothesis. Execute it against the packaged artifact and compatible state.

#### Writing runbooks around implementation details instead of operator-visible symptoms.

Runbooks should begin with symptoms and decisions, not source-module names. Test them with someone who did not write the code.

#### Closing an incident with a patch but no corrected model, regression test, limit, or signal.

A patch closes one incident but not the model defect. Add the corrected invariant, signal, limit, or regression scenario.

## Use the idea in a complete program

```rust
#[derive(Debug)]
struct CapacityModel {
    max_active: usize,
    queue_capacity: usize,
    bytes_per_active: usize,
    bytes_per_queued: usize,
}

impl CapacityModel {
    fn estimated_bytes(&self) -> Option<usize> {
        self.max_active
            .checked_mul(self.bytes_per_active)?
            .checked_add(self.queue_capacity.checked_mul(self.bytes_per_queued)?)
    }
}

fn main() {
    let model = CapacityModel {
        max_active: 64,
        queue_capacity: 256,
        bytes_per_active: 32 * 1024,
        bytes_per_queued: 512,
    };
    assert_eq!(model.estimated_bytes(), Some(2_228_224));
}
```

Use the example readiness table as a living argument, not a checkbox list. For each row, verify that the evidence names the same revision, profile, configuration, and workload as the rollout. If the load report predates a queue-capacity change, it is no longer valid evidence for that capacity claim.

Then choose one unknown. Bound its possible damage, add a signal, define a stop condition, and assign an owner. If you cannot make all four explicit, the unknown is a deployment blocker rather than a monitored risk.

### MetricRail consequence

MetricRail’s readiness case combines its deterministic semantics, memory and identifier budgets, bounded connection and broker admission, load-curve evidence, structured signals, security boundary, artifact manifest, and operations guides. The case is intentionally rejectable: missing authentication/TLS prevents exposure on an untrusted interface.

Capacity planning starts below the observed saturation knee and reserves space for failover and rollout overlap. The rollout guide defines canary population, observation window, p95/p99 and error thresholds, queue and memory limits, stop conditions, and the exact rollback artifact.

The incident drill uses a realistic displaced-cost failure: shared views reduce copies but retain large buffers, while a higher connection limit multiplies retention. The lesson becomes a memory regression scenario and a review question, not merely a post-incident story.

### Boundary case: evidence invalidated by configuration

A release candidate has excellent benchmark and load reports, but the rollout configuration doubles `max_connections` and quadruples the broker mailbox. The evidence was collected under the old envelope. Even though the source revision is unchanged, the capacity and memory claims no longer apply: more connection buffers and queued records can be live simultaneously, and queue residence may change tail behavior.

Treat configuration as part of artifact identity for readiness. Either rerun the relevant load and memory scenarios with the proposed values or retain the validated envelope. The rollout plan must compare the exact runtime configuration, dependency endpoints, and feature set against the evidence ledger.

During canary, define automatic stop conditions before exposure: p99 regression, queue-depth persistence, memory slope, overload rate, invariant errors, or readiness loss. Keep the previous artifact and compatible configuration available. A rollback that requires an emergency rebuild or undocumented data conversion is not a rollback plan. After the exercise, turn every discovered gap into a test, limit, signal, or runbook correction with an owner and expiration date.

## Practice sequence

1. Build a MetricRail claim-to-evidence ledger and mark evidence age and artifact identity.
2. Complete the Production Readiness Review lab, including one explicit rejection.
3. Calculate a capacity envelope with failover and deployment overlap.
4. Rehearse the canary stop and rollback path using the packaged artifact.
5. Run the incident drill from symptoms, not source knowledge.
6. Write the final release decision with accepted risks, owners, expiration dates, and the next evidence-gathering action.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- reject stale evidence that belongs to a different artifact or configuration;
- calculate capacity with burst, skew, failover, rollout overlap, and headroom;
- define staged rollout signals and stop conditions;
- execute rather than merely document rollback;
- turn an incident into a corrected model and regression proof;
- distinguish a bounded owned unknown from an unbounded deployment blocker.

## Primary Rust references

- Cargo and Rust release documentation for the exact artifact under review
- Service-reliability references for capacity planning, staged rollout, incident response, and post-incident learning
- Platform-specific deployment, rollback, health-check, and resource-isolation documentation

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

1. Complete the [Module 90 workbook](workbook.md).
2. Use the [reasoned solutions](solutions.md) only after writing your own answers.
3. Build the [Production Readiness Review laboratory](../../labs/module-10-production-readiness-review/README.md).
4. Apply the module to [MetricRail](../capstone.md).
