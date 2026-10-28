# Course 9 — Rust Performance and Production Engineering

## Measurement, Efficiency, Observability, Security, and Delivery

## The promise

Course 9 converts production claims into falsifiable contracts. It covers benchmark design, profiling, allocation and data movement, saturation and queueing, observability, reliability policy, threat modeling, supply-chain review, Cargo profiles, packaging, rollout, and incident learning.

> **Governing question:** Which measurements, resource bounds, signals, security controls, artifact records, and operating policies make a Rust system defensible under representative load?

Course 8 established a correct, bounded async service. Course 9 asks whether the service’s performance, memory, reliability, observability, security, release, and operating claims are supported by representative evidence. Correctness remains the oracle; measurement and operations add new evidence rather than replacing it.

## Before Day 1

You should be able to build bounded synchronous and asynchronous systems, state protocol and shutdown guarantees, separate live metrics from authoritative state, and preserve deterministic behavior under concurrency.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle.
- Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked.
- Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count.
- Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers.
- Separate service time, wait time, queue depth, concurrency, throughput, and utilization.
- Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer.
- Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous.
- Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service.
- Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy.
- Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery.
- Integrate all ten mechanisms in MetricRail without creating competing authorities.
- Complete and defend an unseen change using a production decision record.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [81 — Performance Contracts, Workloads, and Benchmark Design](./module-81-performance-contracts-workloads-and-benchmark-design/index.md) | What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception? | **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle.** | [Benchmark Integrity Clinic](../labs/module-01-benchmark-integrity-clinic/README.md) |
| 2 | [82 — CPU Profiling, Cost Models, and Hot-Path Optimization](./module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md) | Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase? | **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked.** | [Profile-Guided Query Engine](../labs/module-02-profile-guided-query-engine/README.md) |
| 3 | [83 — Allocation, Memory Footprint, and Ownership Cost](./module-83-allocation-memory-footprint-and-ownership-cost/index.md) | Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost? | **Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count.** | [Allocation-Budgeted Batch Parser](../labs/module-03-allocation-budgeted-batch-parser/README.md) |
| 4 | [84 — Data Movement, Buffering, and Zero-Copy Boundaries](./module-84-data-movement-buffering-and-zero-copy-boundaries/index.md) | Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost? | **Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers.** | [Borrowed Record Window](../labs/module-04-borrowed-record-window/README.md) |
| 5 | [85 — Runtime Efficiency: Contention, Queueing, Batching, and Async Load](./module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md) | When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency? | **Separate service time, wait time, queue depth, concurrency, throughput, and utilization.** | [Bounded Throughput Tuner](../labs/module-05-bounded-throughput-tuner/README.md) |
| 6 | [86 — Observability: Structured Tracing, Metrics, and Diagnostic Context](./module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md) | What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally? | **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer.** | [Structured Observability Harness](../labs/module-06-structured-observability-harness/README.md) |
| 7 | [87 — Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation](./module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md) | How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope? | **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous.** | [Overload Control Simulator](../labs/module-07-overload-control-simulator/README.md) |
| 8 | [88 — Security and Supply-Chain Engineering](./module-88-security-and-supply-chain-engineering/index.md) | Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions? | **Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service.** | [Attack Surface and Supply-Chain Audit](../labs/module-08-attack-surface-and-supply-chain-audit/README.md) |
| 9 | [89 — Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases](./module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md) | How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions? | **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy.** | [Release Matrix and Artifact Manifest](../labs/module-09-release-matrix-and-artifact-manifest/README.md) |
| 10 | [90 — Production Readiness, Capacity Planning, Rollouts, and Incident Learning](./module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) | What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design? | **Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery.** | [Production Readiness Review](../labs/module-10-production-readiness-review/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Claim | State one falsifiable product claim before selecting a benchmark or profiler. |
| Workload | Record scale, skew, data shape, environment, and exclusions. |
| Cost | Separate CPU, allocation, copying, waiting, contention, system calls, and retained state. |
| Signal | Every metric or event answers a named operational question and has a bounded label space. |
| Release | Connect source, lockfile, toolchain, target, profile, features, artifact digest, rollout, and rollback. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **production decision record**. Turn each claim into a representative workload or review procedure, preserve correctness, localize cost or risk, and record the trade-off. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time.

Course 10 synthesizes the entire program: advanced type relationships, compiler representations, unsafe review, verification strategy, compatibility, and long-lived architectural change.

## Capstone — MetricRail

MetricRail is a bounded telemetry aggregator with offline and network paths, representative benchmarks, profiling hooks, memory and byte ledgers, structured tracing, overload policy, security and dependency records, release manifests, runbooks, and rollout exercises.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Take a bounded service and produce a complete production dossier: benchmark protocol, profile, memory and byte accounting, load curve, observability map, reliability policy, threat model, release manifest, and go/no-go decision.

and then change the capstone under this constraint:

> Add one high-cardinality MetricRail query while preserving bounded memory, deterministic output, observability cardinality, overload behavior, and artifact traceability.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 81 — Performance Contracts, Workloads, and Benchmark Design](./module-81-performance-contracts-workloads-and-benchmark-design/index.md)
- [MetricRail engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
