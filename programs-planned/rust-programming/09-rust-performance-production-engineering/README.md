# Rust Performance and Production Engineering

## Measurement, Efficiency, Observability, Security, and Delivery

This is Course 9 of the Rust Programming path and covers Modules 81–90. The first eight courses taught how to construct typed programs, reason about ownership and memory, design trait-based architecture, express dataflow, extend syntax at compile time, cross systems boundaries, coordinate concurrent work, and build asynchronous network services.

Course 9 asks a different question:

> How do you know that the program is efficient, bounded, diagnosable, secure, reproducible, and safe to operate under the workload it will actually receive?

The course does not reduce production engineering to optimization. Speed matters only in relation to a product operation, a workload, a resource envelope, and preserved semantics. Observability matters only when its signals answer operational questions without exposing secrets or exhausting storage. Reliability matters only when admission, retry, degradation, and recovery policies are explicit. A release matters only when the artifact can be traced to reviewed inputs and installed, upgraded, rolled back, and diagnosed.

The cumulative capstone, **MetricRail**, is a bounded telemetry aggregation service. It begins as a correct service and is progressively benchmarked, profiled, made allocation-aware, instrumented, hardened against overload and hostile input, packaged, and prepared for staged operation. This inversion is deliberate: the course teaches how to take a functioning system to a defensible production state.

## The production-engineering loop

Every module uses the same causal loop:

```text
state the product claim
        ↓
choose the authoritative behavior
        ↓
design a representative workload
        ↓
measure or model the current system
        ↓
localize the dominant cause or risk
        ↓
change one mechanism
        ↓
remeasure and revalidate
        ↓
record the trade-off and operating policy
```

Skipping the first three steps creates benchmark theater. Skipping revalidation creates semantic drift. Skipping the operating policy leaves the change impossible to manage under failure.

## Prerequisites

Start this course when you can:

- build and test a multi-crate Rust application;
- explain ownership, borrowing, allocation, synchronization, async cancellation, and bounded queues;
- distinguish a language guarantee, library contract, target observation, and product policy;
- design a versioned hostile-input parser with explicit size limits;
- own and join thread and task lifecycles;
- implement admission, deadlines, cancellation, and graceful shutdown;
- read Cargo manifests and reason about features, profiles, and lockfiles;
- maintain a correctness oracle while changing an implementation.

The [course overview](course-book/index.md) contains a readiness diagnosis and repair route.

## Ten modules

81. [Performance Contracts, Workloads, and Benchmark Design](course-book/module-81-performance-contracts-workloads-and-benchmark-design/index.md) — What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?
82. [CPU Profiling, Cost Models, and Hot-Path Optimization](course-book/module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md) — Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?
83. [Allocation, Memory Footprint, and Ownership Cost](course-book/module-83-allocation-memory-footprint-and-ownership-cost/index.md) — Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?
84. [Data Movement, Buffering, and Zero-Copy Boundaries](course-book/module-84-data-movement-buffering-and-zero-copy-boundaries/index.md) — Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?
85. [Runtime Efficiency: Contention, Queueing, Batching, and Async Load](course-book/module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md) — When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency?
86. [Observability: Structured Tracing, Metrics, and Diagnostic Context](course-book/module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md) — What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?
87. [Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation](course-book/module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md) — How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?
88. [Security and Supply-Chain Engineering](course-book/module-88-security-and-supply-chain-engineering/index.md) — Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?
89. [Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases](course-book/module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md) — How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?
90. [Production Readiness, Capacity Planning, Rollouts, and Incident Learning](course-book/module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) — What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?

## How to study

One module is one dense day. Follow this order:

```text
authoritative chapter
    → frozen predictions
    → causal repair
    → focused exercises
    → independent laboratory
    → MetricRail increment
    → reconstruction and defense
```

Do not begin by copying a reference solution or adjusting profile flags. Write the product claim and expected causal mechanism first. A surprising result is useful only when the experiment can explain what was actually tested.

## Course surfaces

- [Course-book overview](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Production engineering reference](course-book/reference.md)
- [MetricRail engineering guide](course-book/capstone.md)
- [Final review](course-book/final-review.md)
- [Compiler investigations](compiler-labs/README.md)
- [Laboratories](labs/)

## Tooling

The course pins exact dependency versions for reproducibility within the teaching release:

- Criterion 0.8.2 for statistical microbenchmarks;
- Bytes 1.12.1 for shared byte buffers and views;
- Tokio 1.53.1 for the async capstone;
- Tracing 0.1.44 and tracing-subscriber 0.3.23 for structured diagnostics.

These dependencies are used where they teach a real production mechanism. Most focused examples and several labs remain standard-library-only.

## Primary commands

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make fmt
make clippy
make docs
make proof
```

`make proof` is the strongest route and requires Rust, Cargo, rustfmt, Clippy, rustdoc, and MkDocs.

## Continue

Begin with the [course overview and readiness diagnosis](course-book/index.md), then follow the [ten-day study plan](course-book/study-plan.md).
