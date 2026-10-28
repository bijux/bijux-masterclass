# Rust Performance and Production Engineering

Course 9 covers Modules 81–90. It begins where a conventional programming course often stops: the system is functionally correct, tested, concurrent, and networked. The remaining work is to make its cost, failure behavior, observability, security posture, artifact identity, and operational envelope explicit.

## What this course is about

Production engineering is not a miscellaneous final chapter containing benchmarking, logging, and deployment tips. It is the discipline of turning implementation behavior into claims that can be tested and operated.

A production claim must answer:

- **What behavior is authoritative?**
- **Which workload and boundary are being discussed?**
- **Which resources are bounded?**
- **Which result is measured rather than guaranteed?**
- **What happens under overload, dependency failure, malicious input, and partial rollout?**
- **Which artifact and configuration were actually tested?**
- **How is a bad change detected, stopped, and reversed?**

The course-book is the primary learning route. Each chapter develops one complete reasoning model, then applies it to a small program and to MetricRail. The workbooks test prediction, diagnosis, independent construction, transfer, and defense. Labs isolate mechanisms so you can see them clearly before they interact in the capstone.

## What you will be able to do

After completing the course, you will be able to:

- define performance and production requirements as falsifiable contracts rather than vague aspirations
- design benchmarks whose workload, boundary, oracle, environment, and statistical interpretation are explicit
- use profiles and scaling models to identify causal costs before editing hot code
- quantify allocation frequency, live memory, retained capacity, and ownership-driven lifetime cost
- trace byte movement and choose deliberate borrow, share, move, or copy boundaries
- measure saturation, queueing, contention, batching, and asynchronous scheduling under representative load
- design structured traces, bounded metrics, health semantics, and redaction rules from operational questions
- connect service-level objectives to admission, retries, degradation, and recovery policy
- threat-model a Rust service and review dependencies, build scripts, privileges, secrets, and release provenance
- choose Cargo profiles, feature matrices, targets, packaging, and CI checks as explicit product variants
- derive capacity and rollout policy from measured resource demand and failure behavior
- prepare and defend a complete production-readiness review for a specific artifact and workload envelope

## Readiness diagnosis

Before Module 81, answer these questions without running code:

1. Why can a lower average latency coexist with a worse p99?
2. Why does `size_of::<Vec<T>>()` not describe the vector’s total memory cost?
3. When can a borrowed 20-byte slice retain a much larger allocation?
4. Why can increasing queue capacity lower rejection while worsening reliability?
5. What is the difference between an event, a span, a metric, and an audit record?
6. Why can a retry execute an operation twice even after the client observed a timeout?
7. Which claims about binary layout or operating-system copying are target observations rather than Rust guarantees?
8. What inputs determine a Cargo artifact?
9. What is the difference between liveness and readiness?
10. Why must rollback be rehearsed rather than merely documented?

If several answers are uncertain, revisit the relevant Course 2, 6, 7, and 8 chapters. This course assumes the underlying mechanisms and concentrates on product-level evidence.

## The course narrative

### Days 1–3: establish cost truth

Modules 81–83 move from benchmark contract to profile to memory lifecycle. The reader learns to reject optimization by intuition. The output is a performance charter, representative corpora, causal profiles, and an allocation ledger.

### Days 4–5: make movement and waiting explicit

Modules 84–85 trace bytes and load through buffers, queues, locks, tasks, batches, and service phases. The output is an honest byte journey and a measured saturation envelope.

### Days 6–8: make operation and risk explicit

Modules 86–88 design production signals, reliability policies, and security controls. The output is a diagnosable service with bounded labels, typed overload, controlled retries, degraded modes, a threat model, and a dependency policy.

### Days 9–10: make delivery and operation explicit

Modules 89–90 define the artifact, CI matrix, release manifest, installation route, capacity plan, rollout, rollback, runbooks, and incident-learning loop.

## The claim ledger

Maintain one ledger throughout the course:

| Claim | Class | Authority | Workload or scope | Bound | Evidence | Owner |
|---|---|---|---|---|---|---|
| Snapshot order is stable | semantic | public API | all inputs | n/a | integration tests | library |
| Ingestion p95 meets target | measured | performance charter | corpus v1, reference host | target only | benchmark report | performance owner |
| Queue accepts at most 1024 jobs | resource | configuration and queue type | all traffic | 1024 | tests and metrics | service |
| Token fields never appear in logs | security | event schema | all log paths | no disclosure | redaction tests | observability |
| Artifact matches source revision | release | manifest | one release | digest | CI output | release owner |

Add or revise rows after every module. If a claim has no authority or evidence, it is an assumption.

## Modules

81. [Performance Contracts, Workloads, and Benchmark Design](module-81-performance-contracts-workloads-and-benchmark-design/index.md) — What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?
82. [CPU Profiling, Cost Models, and Hot-Path Optimization](module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md) — Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?
83. [Allocation, Memory Footprint, and Ownership Cost](module-83-allocation-memory-footprint-and-ownership-cost/index.md) — Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?
84. [Data Movement, Buffering, and Zero-Copy Boundaries](module-84-data-movement-buffering-and-zero-copy-boundaries/index.md) — Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?
85. [Runtime Efficiency: Contention, Queueing, Batching, and Async Load](module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md) — When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency?
86. [Observability: Structured Tracing, Metrics, and Diagnostic Context](module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md) — What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?
87. [Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation](module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md) — How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?
88. [Security and Supply-Chain Engineering](module-88-security-and-supply-chain-engineering/index.md) — Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?
89. [Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases](module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md) — How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?
90. [Production Readiness, Capacity Planning, Rollouts, and Incident Learning](module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) — What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?

## The independent laboratories

The ten labs are intentionally different products:

1. Benchmark Integrity Clinic
2. Profile-Guided Query Engine
3. Allocation-Budgeted Batch Parser
4. Borrowed Record Window
5. Bounded Throughput Tuner
6. Structured Observability Harness
7. Overload Control Simulator
8. Attack Surface and Supply-Chain Audit
9. Release Matrix and Artifact Manifest
10. Production Readiness Review

Each lab has a starter and a reference implementation. Use the reference only after your own model, predictions, implementation, and result are written.

## The cumulative capstone

[MetricRail](capstone.md) receives telemetry records:

```text
tenant<TAB>metric<TAB>timestamp_ms<TAB>value
```

It aggregates bounded series statistics and offers deterministic snapshots through a CLI and a small TCP service. The product is simple enough for end-to-end reasoning but exposes realistic production concerns:

- skewed and malformed workloads;
- allocation and key retention;
- byte framing and buffering;
- queueing and contention;
- structured tracing and bounded metrics;
- overload and degradation;
- tenant and operator boundaries;
- exact dependencies and profiles;
- release manifests;
- capacity and rollout decisions.

## Completion standard

You have not completed the course merely because MetricRail builds or because a benchmark improved. Completion means you can:

- state the claim and workload before measuring;
- explain the dominant cost or risk causally;
- preserve the semantic oracle;
- show where cost or responsibility moved;
- classify the result as guarantee, policy, or observation;
- set explicit resource bounds;
- produce an installable traceable artifact;
- defend rollout and recovery behavior.

## Continue

Use the [ten-day study plan](study-plan.md). Keep the [reference desk](reference.md) nearby for units, formulas, signal types, and release terminology. Do not read the [final review](final-review.md) until you have completed the ten module reconstructions.
