# Course 9 — Rust Performance and Production Engineering

## Measurement, Efficiency, Observability, Security, and Delivery

Course 9 converts production claims into falsifiable contracts. It covers benchmark design, profiling, allocation and data movement, saturation and queueing, observability, reliability policy, threat modeling, supply-chain review, Cargo profiles, packaging, rollout, and incident learning.

> **Governing question:** Which measurements, resource bounds, signals, security controls, artifact records, and operating policies make a Rust system defensible under representative load?

## Entry point

You should be able to build bounded synchronous and asynchronous systems, state protocol and shutdown guarantees, separate live metrics from authoritative state, and preserve deterministic behavior under concurrency.

The immediate prerequisite is [Course 8: Rust Async and Networked Services](../08-rust-async-networked-services/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [81 — Performance Contracts, Workloads, and Benchmark Design](course-book/module-81-performance-contracts-workloads-and-benchmark-design/index.md) | Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle | [Benchmark Integrity Clinic](labs/module-01-benchmark-integrity-clinic/README.md) |
| 2 | [82 — CPU Profiling, Cost Models, and Hot-Path Optimization](course-book/module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md) | Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked | [Profile-Guided Query Engine](labs/module-02-profile-guided-query-engine/README.md) |
| 3 | [83 — Allocation, Memory Footprint, and Ownership Cost](course-book/module-83-allocation-memory-footprint-and-ownership-cost/index.md) | Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count | [Allocation-Budgeted Batch Parser](labs/module-03-allocation-budgeted-batch-parser/README.md) |
| 4 | [84 — Data Movement, Buffering, and Zero-Copy Boundaries](course-book/module-84-data-movement-buffering-and-zero-copy-boundaries/index.md) | Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers | [Borrowed Record Window](labs/module-04-borrowed-record-window/README.md) |
| 5 | [85 — Runtime Efficiency: Contention, Queueing, Batching, and Async Load](course-book/module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md) | Separate service time, wait time, queue depth, concurrency, throughput, and utilization | [Bounded Throughput Tuner](labs/module-05-bounded-throughput-tuner/README.md) |
| 6 | [86 — Observability: Structured Tracing, Metrics, and Diagnostic Context](course-book/module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md) | Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer | [Structured Observability Harness](labs/module-06-structured-observability-harness/README.md) |
| 7 | [87 — Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation](course-book/module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md) | Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous | [Overload Control Simulator](labs/module-07-overload-control-simulator/README.md) |
| 8 | [88 — Security and Supply-Chain Engineering](course-book/module-88-security-and-supply-chain-engineering/index.md) | Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service | [Attack Surface and Supply-Chain Audit](labs/module-08-attack-surface-and-supply-chain-audit/README.md) |
| 9 | [89 — Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases](course-book/module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md) | Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy | [Release Matrix and Artifact Manifest](labs/module-09-release-matrix-and-artifact-manifest/README.md) |
| 10 | [90 — Production Readiness, Capacity Planning, Rollouts, and Incident Learning](course-book/module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) | Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery | [Production Readiness Review](labs/module-10-production-readiness-review/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Turn each claim into a representative workload or review procedure, preserve correctness, localize cost or risk, and record the trade-off. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — MetricRail

MetricRail is a bounded telemetry aggregator with offline and network paths, representative benchmarks, profiling hooks, memory and byte ledgers, structured tracing, overload policy, security and dependency records, release manifests, runbooks, and rollout exercises.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time.

Course 10 synthesizes the entire program: advanced type relationships, compiler representations, unsafe review, verification strategy, compatibility, and long-lived architectural change.

## Exit standard

Complete this independent construction:

> Take a bounded service and produce a complete production dossier: benchmark protocol, profile, memory and byte accounting, load curve, observability map, reliability policy, threat model, release manifest, and go/no-go decision.

Then complete this capstone extension:

> Add one high-cardinality MetricRail query while preserving bounded memory, deterministic output, observability cardinality, overload behavior, and artifact traceability.

The next step is [Course 10: Advanced Rust Mastery](../10-rust-advanced-mastery/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
